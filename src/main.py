from src.agent.workflow import create_agent_workflow, draw_agent_workflow
from src.utils.env import load_env

load_env()


def main() -> None:
    """Main function of the program."""
    # Run the agent
    email_input = {
        "author": "Alice Smith <alice.smith@company.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Quick question about API documentation",
        "email_thread": """Hi John,

    I was reviewing the API documentation for the new authentication service and noticed a few endpoints\n
    seem to be missing from the specs. Could you help clarify if this was intentional or if we should update the docs?

    Specifically, I'm looking at:
    - /auth/refresh
    - /auth/validate

    Thanks!
    Alice""",
    }

    email_agent = create_agent_workflow()
    draw_agent_workflow(email_agent)

    response = email_agent.invoke({"email_input": email_input})
    for message in response["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    main()
