from typing import TypedDict

DEFAULT_HOST = "http://localhost:11434"

class Agent(TypedDict):
    name: str # the name of the agent
    objective: str # what the agent should do e.g. "Debate the chicken or the egg with the other AI"
    model: str # optional, model to use for this specific agent, if not provided use default
    host: str # optional, client to use, e.g http://localhost:11434, by default all models use same host

AgentDetails = tuple[Agent, Agent]