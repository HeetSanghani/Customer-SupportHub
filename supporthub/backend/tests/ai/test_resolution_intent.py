"""Unit tests for Resolution Intent Detection and Ticket Auto-Resolution."""
import pytest
from app.ai.intent import is_resolution_intent
from app.models import Ticket, TicketStatus, User, TicketPriority
from app.services.ai.live_chat_adapter import live_chat_ai_adapter
from app.database import AsyncSessionLocal


def test_positive_resolution_got_answer():
    """Verify variations of 'got my answer' trigger resolution."""
    assert is_resolution_intent("thanks , i got my answer") is True
    assert is_resolution_intent("thanks i got my answer") is True
    assert is_resolution_intent("i got my answer") is True
    assert is_resolution_intent("got my answer") is True
    assert is_resolution_intent("thank you, i got the answer") is True
    assert is_resolution_intent("Got my answer, thanks a lot!") is True
    assert is_resolution_intent("thanks, got what i needed") is True


def test_positive_resolution_question_answered_doubt_cleared():
    """Verify phrases stating questions answered or doubts cleared."""
    assert is_resolution_intent("that answered my question") is True
    assert is_resolution_intent("that answers my question, thank you") is True
    assert is_resolution_intent("my question is answered") is True
    assert is_resolution_intent("all questions answered, thanks") is True
    assert is_resolution_intent("my doubt is cleared") is True
    assert is_resolution_intent("doubt cleared, thank you") is True
    assert is_resolution_intent("understood now, thanks") is True
    assert is_resolution_intent("that's all i needed") is True


def test_positive_resolution_mark_completed_close_ticket():
    """Verify explicit commands to close / complete / resolve ticket."""
    assert is_resolution_intent("mark as completed") is True
    assert is_resolution_intent("mark as resolved") is True
    assert is_resolution_intent("mark the ticket as completed") is True
    assert is_resolution_intent("mark this ticket as completed") is True
    assert is_resolution_intent("mark ticket as resolved") is True
    assert is_resolution_intent("close the ticket") is True
    assert is_resolution_intent("you can close this ticket") is True
    assert is_resolution_intent("resolve this ticket") is True
    assert is_resolution_intent("problem solved") is True
    assert is_resolution_intent("that fixed it") is True


def test_negative_guards_not_resolution():
    """Verify questions and negative statements do not trigger resolution."""
    assert is_resolution_intent("why was my ticket closed?") is False
    assert is_resolution_intent("how do i close my account?") is False
    assert is_resolution_intent("can you answer my question?") is False
    assert is_resolution_intent("i did not get my answer") is False
    assert is_resolution_intent("i haven't got my answer yet") is False
    assert is_resolution_intent("problem not solved") is False
    assert is_resolution_intent("what is your refund policy?") is False
    assert is_resolution_intent("where is my order ORD-001") is False

