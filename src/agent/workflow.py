from IPython.display import Image
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from src.models.state import State
from src.nodes.prompt import create_prompt
from src.nodes.triage import triage_router
from src.tools.mail import check_calendar_availability, schedule_meeting, write_email


def create_agent_workflow() -> CompiledGraph:
    """
    Create the agent workflow for the email agent.

    Returns
    -------
    CompiledGraph:
        The compiled agent workflow.
    """
    agent = get_agent()
    email_agent = StateGraph(State)
    email_agent = email_agent.add_node(triage_router)
    email_agent = email_agent.add_node("response_agent", agent)
    email_agent = email_agent.add_edge(START, "triage_router")
    email_agent = email_agent.compile()

    return email_agent


def get_agent() -> CompiledGraph:
    """
    Get the agent for the email agent workflow.

    Returns
    -------
    CompiledGraph:
        The compiled agent.
    """
    tools = get_tools()
    agent = create_react_agent(
        "openai:gpt-4o",
        tools=tools,
        prompt=create_prompt,
    )

    return agent


def get_tools() -> list[tool]:
    """
    Get the list of tools for the agent.

    Returns
    -------
    list[tool]:
        List of tools for the agent.
    """
    tools = [write_email, schedule_meeting, check_calendar_availability]

    return tools


def draw_agent_workflow(agent: CompiledGraph) -> None:
    """Draw the agent workflow."""
    Image(
        agent.get_graph(xray=True).draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,  # MermaidDrawMethod.PYPPETEER,
            curve_style=CurveStyle.LINEAR,
            node_colors=NodeStyles(first="#ffdfba", last="#baffc9", default="#fad7de"),
            wrap_label_n_words=9,
            background_color="transparent",
            padding=10,
            output_file_path="img/agent_workflow.png",
        )
    )
