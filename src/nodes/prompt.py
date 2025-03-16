from src.constants import agent_system_prompt, profile, prompt_instructions
from src.models.state import State


def create_prompt(state: State) -> list[dict]:
    """
    Create the prompt for the agent.
    Parameters:
    -----------
    state: State
        The current state of the agent.

    Returns:
    --------
    list[dict]:
        The prompt for the agent.
    """
    return [
        {
            "role": "system",
            "content": agent_system_prompt.format(
                instructions=prompt_instructions["agent_instructions"],
                **profile
                )
        }
    ] + state['messages']