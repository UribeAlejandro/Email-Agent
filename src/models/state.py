from typing_extensions import TypedDict, Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    """State of the agent."""
    email_input: str
    messages: Annotated[list, add_messages]
