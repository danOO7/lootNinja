"""
Simple Request Agent - A basic agent for handling user requests and questions.
"""
from textwrap import dedent
import logging
import os

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.ag_ui import StateDeps
from ag_ui.core import EventType, StateSnapshotEvent
from pydantic_ai.models.openai import OpenAIResponsesModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====
# State Models
# =====
class Message(BaseModel):
    """A chat message."""
    role: str = Field(description="'user' or 'assistant'")
    content: str = Field(description="The message content")


class RequestState(BaseModel):
    """Simple request agent state."""
    user_request: str = Field(
        default="",
        description="The user's request or question"
    )
    messages: list[Message] = Field(
        default_factory=list,
        description="Conversation history"
    )
    response: str = Field(
        default="",
        description="The agent's response"
    )


# =====
# Agent Definition
# =====
agent = Agent(
    model=OpenAIResponsesModel('gpt-4o-mini'),
    deps_type=StateDeps[RequestState],
    system_prompt=dedent("""
        You are a helpful and friendly assistant.
        
        Your role is to:
        1. Listen carefully to user requests
        2. Provide clear, concise, and helpful responses
        3. Ask clarifying questions if needed
        4. Be conversational and engaging
        
        Always aim to be helpful, honest, and direct in your responses.
    """).strip()
)


# =====
# Tools
# =====
@agent.tool
def add_message(
    ctx: RunContext[StateDeps[RequestState]],
    role: str,
    content: str
) -> StateSnapshotEvent:
    """
    Add a message to the conversation history.
    
    Args:
        role: 'user' or 'assistant'
        content: The message content
    """
    try:
        msg = Message(role=role, content=content)
        ctx.deps.state.messages.append(msg)
        logger.info(f"Added {role} message: {content[:50]}...")
        
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )
    except Exception as e:
        logger.error(f"Error adding message: {e}")
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )


@agent.tool
def get_messages(ctx: RunContext[StateDeps[RequestState]]) -> list[dict]:
    """
    Get the conversation history.
    
    Returns:
        List of messages with role and content
    """
    return [{"role": m.role, "content": m.content} for m in ctx.deps.state.messages]


@agent.tool
async def set_response(
    ctx: RunContext[StateDeps[RequestState]],
    response: str
) -> StateSnapshotEvent:
    """
    Set the agent's response to the user request.
    
    Args:
        response: The agent's response text
    """
    try:
        ctx.deps.state.response = response
        logger.info(f"Response set: {response[:50]}...")
        
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )
    except Exception as e:
        logger.error(f"Error setting response: {e}")
        return StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=ctx.deps.state,
        )


@agent.tool
def get_response(ctx: RunContext[StateDeps[RequestState]]) -> str:
    """
    Get the current response.
    
    Returns:
        The agent's response text
    """
    return ctx.deps.state.response
