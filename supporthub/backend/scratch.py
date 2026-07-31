import os
import asyncio
import google.generativeai as genai
from google.protobuf.struct_pb2 import Struct
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def test_tools(ticket_id: str):
    async def resolve_ticket():
        """Resolves the current ticket if the customer is satisfied."""
        await asyncio.sleep(0.1)
        print(f"RESOLVING TICKET {ticket_id} ASYNC!")
        return "Ticket marked as resolved."

    model = genai.GenerativeModel("gemini-2.5-flash", tools=[resolve_ticket])
    chat = model.start_chat()
    async def run():
        res = await chat.send_message_async("I am satisfied. Please resolve this ticket.")
        for part in res.parts:
            if fn_call := part.function_call:
                print("Function call requested:", fn_call.name)
                ret = await resolve_ticket()
                
                s = Struct()
                s.update({"result": ret})
                
                res2 = await chat.send_message_async(
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
                print("Final answer:", res2.text)
    
    asyncio.run(run())

test_tools("TCK-123")
