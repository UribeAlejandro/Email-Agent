from typing import Literal

from langchain.chat_models import init_chat_model
from langgraph.graph import END
from langgraph.types import Command

from src.constants import profile, prompt_instructions, triage_system_prompt, triage_user_prompt
from src.models.router import Router
from src.models.state import State


def triage_router(state: State) -> Command[Literal["response_agent", "__end__"]]:
    """
    Triage the email and determine its classification.

    Parameters
    ----------
    state: State
        The current state of the agent.

    Returns
    -------
    Command[Literal["response_agent", "__end__"]]:
        The command to execute based on the classification.
    """
    author = state["email_input"]["author"]  # type: ignore
    to = state["email_input"]["to"]  # type: ignore
    subject = state["email_input"]["subject"]  # type: ignore
    email_thread = state["email_input"]["email_thread"]  # type: ignore

    llm = init_chat_model("openai:gpt-4o-mini")
    llm_router = llm.with_structured_output(Router)

    system_prompt = triage_system_prompt.format(
        full_name=profile["full_name"],
        name=profile["name"],
        user_profile_background=profile["user_profile_background"],
        triage_no=prompt_instructions["triage_rules"]["ignore"],
        triage_notify=prompt_instructions["triage_rules"]["notify"],
        triage_email=prompt_instructions["triage_rules"]["respond"],
        examples=None,
    )
    user_prompt = triage_user_prompt.format(author=author, to=to, subject=subject, email_thread=email_thread)
    result = llm_router.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    if result.classification == "respond":
        print("📧 Classification: RESPOND - This email requires a response")
        goto = "response_agent"
        update = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Respond to the email {state['email_input']}",
                }
            ]
        }
    elif result.classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
        update = None
        goto = END
    elif result.classification == "notify":
        # If real life, this would do something else
        print("🔔 Classification: NOTIFY - This email contains important information")
        update = None
        goto = END
    else:
        raise ValueError(f"Invalid classification: {result.classification}")
    return Command(goto=goto, update=update)
