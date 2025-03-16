from typing import Annotated

from langgraph.graph import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    """State of the agent."""

    email_input: str
    messages: Annotated[list, add_messages]
