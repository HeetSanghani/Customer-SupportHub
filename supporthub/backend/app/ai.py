from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
from app.config import get_settings

settings = get_settings()

if hasattr(settings, "gemini_api_key") and settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)
elif os.environ.get("GEMINI_API_KEY"):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_embedding(text: str) -> list[float]:
    """Generates an embedding vector using Gemini API and pads it to 1536 dims."""
    if not os.environ.get("GEMINI_API_KEY") and not getattr(settings, "gemini_api_key", None):
        # Fallback to mock embedding if no key is set
        import random
        return [random.uniform(-0.1, 0.1) for _ in range(1536)]
        
    result = genai.embed_content(
        model="models/gemini-embedding-2",
        content=text,
        task_type="retrieval_document"
    )
    vec = result['embedding']
    
    # Gemini returns 768 dimensions. Our db schema uses 1536 (OpenAI standard).
    # We pad the remaining 768 with zeros so pgvector accepts it, which
    # preserves the cosine similarity math perfectly!
    if len(vec) < 1536:
        vec.extend([0.0] * (1536 - len(vec)))
    elif len(vec) > 1536:
        vec = vec[:1536]
    
    return vec

async def generate_chat_response(prompt: str) -> str:
    """Generates a chat response using Gemini Flash Lite."""
    model = genai.GenerativeModel("gemini-flash-lite-latest")
    response = await model.generate_content_async(prompt)
    return response.text

async def generate_rag_response(session, user_query: str, ticket_id: str = None) -> str:
    """
    1. Embeds the user query.
    2. Uses pgvector to find the top 2 most relevant KbArticles.
    3. Asks Gemini to answer the query, executing tools (Phase 6) if the user is satisfied or angry.
    """
    from sqlalchemy import select
    from app.models import KbArticle, Ticket, TicketStatus, TicketPriority
    import asyncio
    import uuid
    from google.protobuf.struct_pb2 import Struct
    from google.generativeai.types import content_types
    
    # 1. Embed query
    query_vec = await asyncio.to_thread(generate_embedding, user_query)
    
    # 2. Vector search (cosine distance <->)
    stmt = (
        select(KbArticle)
        .where(KbArticle.published == True)
        .order_by(KbArticle.embedding.cosine_distance(query_vec))
        .limit(2)
    )
    result = await session.execute(stmt)
    articles = result.scalars().all()
    
    # Phase 6: Define Tools
    async def resolve_ticket(new_subject: str = None):
        """Use this tool to resolve the ticket if the customer states their issue is fixed or they are satisfied. Optionally provide a short new_subject to rename the ticket if it's currently 'New Support Query'."""
        if ticket_id:
            ticket = await session.get(Ticket, uuid.UUID(ticket_id))
            if ticket:
                ticket.status = TicketStatus.resolved
                ticket.ai_resolved = True
                if new_subject and ticket.subject == "New Support Query":
                    ticket.subject = new_subject
                await session.commit()
                return "Successfully resolved the ticket."
        return "Failed to resolve ticket."

    async def escalate_ticket(new_subject: str = None):
        """Use this tool to escalate the ticket to a human manager if the customer is very angry, frustrated, or demands to speak to a human. Optionally provide a short new_subject to rename the ticket if it's currently 'New Support Query'."""
        if ticket_id:
            ticket = await session.get(Ticket, uuid.UUID(ticket_id))
            if ticket:
                ticket.status = TicketStatus.escalated
                ticket.priority = TicketPriority.high
                if new_subject and ticket.subject == "New Support Query":
                    ticket.subject = new_subject
                await session.commit()
                return "Successfully escalated the ticket to a human."
        return "Failed to escalate ticket."

    async def update_priority(priority: str, new_subject: str = None):
        """Use this tool to update the priority of the ticket to 'urgent' if the customer is facing a critical emergency or server downtime. Optionally provide a short new_subject to rename the ticket if it's currently 'New Support Query'."""
        if ticket_id:
            ticket = await session.get(Ticket, uuid.UUID(ticket_id))
            if ticket:
                if priority.lower() == 'urgent':
                    ticket.priority = TicketPriority.urgent
                if new_subject and ticket.subject == "New Support Query":
                    ticket.subject = new_subject
                await session.commit()
                return f"Successfully updated priority."
        return "Priority updated."

    async def rename_ticket(new_subject: str):
        """Use this tool to rename the ticket subject to something descriptive if the current subject is 'New Support Query'."""
        if ticket_id:
            ticket = await session.get(Ticket, uuid.UUID(ticket_id))
            if ticket and ticket.subject == "New Support Query":
                ticket.subject = new_subject
                await session.commit()
                return f"Successfully renamed ticket to {new_subject}."
        return "Ticket already has a descriptive name or couldn't be renamed."

    # Map function names to their async handlers
    tools_map = {
        "resolve_ticket": resolve_ticket,
        "escalate_ticket": escalate_ticket,
        "update_priority": update_priority,
        "rename_ticket": rename_ticket
    }

    # 3. Construct prompt
    context_text = "\n\n".join([f"Title: {a.title}\n{a.body}" for a in articles])
    
    prompt = f"""You are a helpful Customer Support AI Agent. 
Use the following Knowledge Base articles to answer the user's question.
If the answer is not in the articles, say "I don't have enough information to answer that, but I will connect you with a human agent shortly." Do not invent facts.

If the user is satisfied, call the resolve_ticket tool.
If the user is very angry or requests a human, call the escalate_ticket tool.
If the user mentions a critical outage or emergency, call the update_priority tool with 'urgent'.
If this is the very first message of a new conversation (i.e. the ticket is called "New Support Query"), you MUST rename it to a short (2-5 words) descriptive title. You can do this by either calling the rename_ticket tool directly, OR if you are calling resolve_ticket, escalate_ticket, or update_priority, you MUST pass the 'new_subject' parameter to them simultaneously.

Knowledge Base:
{context_text}

User Question: {user_query}
"""

    model = genai.GenerativeModel("gemini-flash-lite-latest", tools=[resolve_ticket, escalate_ticket, update_priority, rename_ticket])
    chat = model.start_chat()
    
    # Send the initial prompt
    res = await chat.send_message_async(prompt)
    
    # Check if the AI wants to call a function
    for part in res.parts:
        if fn_call := part.function_call:
            if fn_call.name in tools_map:
                # Call the mapped async function
                # Extract arguments dynamically
                kwargs = {k: v for k, v in fn_call.args.items()}
                ret_val = await tools_map[fn_call.name](**kwargs)
                
                # Construct Struct response
                s = Struct()
                s.update({"result": ret_val})
                
                # Send function response back to Gemini
                res = await chat.send_message_async(
                    genai.protos.Content(
                        parts=[
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=fn_call.name,
                                    response=s
                                )
                            )
                        ]
                    )
                )
                
    return res.text


async def generate_ai_ticket_subject(session, ticket_id) -> str:
    """Analyzes the conversation transcript of a ticket and generates a concise, descriptive subject (3-6 words) using Gemini."""
    from sqlalchemy import select
    from app.models import Ticket, Message
    import uuid

    try:
        ticket_uuid = uuid.UUID(ticket_id) if isinstance(ticket_id, str) else ticket_id
        ticket = await session.get(Ticket, ticket_uuid)
        if not ticket:
            return ""

        stmt = select(Message).where(Message.ticket_id == ticket_uuid).order_by(Message.created_at.asc())
        messages = (await session.execute(stmt)).scalars().all()
        if not messages:
            return ""

        conversation_lines = []
        for m in messages:
            sender = m.sender_type.value if hasattr(m.sender_type, "value") else str(m.sender_type)
            if m.body and m.body.strip():
                conversation_lines.append(f"{sender.capitalize()}: {m.body.strip()}")

        if not conversation_lines:
            return ""

        transcript = "\n".join(conversation_lines[-12:])

        prompt = f"""Analyze the following customer support conversation and generate a concise, highly descriptive subject line (3 to 6 words maximum) that accurately summarizes the main topic of the conversation.
Do NOT use quotes, markdown, or trailing periods. Respond ONLY with the subject title.

Conversation:
{transcript}
"""
        model = genai.GenerativeModel("gemini-flash-lite-latest")
        res = await model.generate_content_async(prompt)
        ai_subject = res.text.strip().replace('"', '').replace('*', '').strip()
        if ai_subject and len(ai_subject) >= 3:
            ticket.subject = ai_subject
            session.add(ticket)
            await session.commit()
            return ai_subject
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("Failed to auto-generate AI ticket subject: %s", e)
    return ""

