import json

with open("conf/prompts/agent_system_prompt.txt", "r") as f:
    agent_system_prompt = f.read()

with open("conf/prompts/triage_system_prompt.txt", "r") as f:
    triage_system_prompt = f.read()

with open("conf/prompts/triage_user_prompt.txt", "r") as f:
    triage_user_prompt = f.read()

profile = json.load(open("conf/profile.json"))
prompt_instructions = json.load(open("conf/prompt_instructions.json"))
email = json.load(open("conf/email.json"))

system_prompt = triage_system_prompt.format(
    full_name=profile["full_name"],
    name=profile["name"],
    examples=None,
    user_profile_background=profile["user_profile_background"],
    triage_no=prompt_instructions["triage_rules"]["ignore"],
    triage_notify=prompt_instructions["triage_rules"]["notify"],
    triage_email=prompt_instructions["triage_rules"]["respond"],
)

user_prompt = triage_user_prompt.format(
    author=email["from"],
    to=email["to"],
    subject=email["subject"],
    email_thread=email["body"],
)