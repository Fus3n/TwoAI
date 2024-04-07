from typing import TypedDict, Annotated

class Agent(TypedDict):
    name: str # the name of the agent
    objective: str # what the agent should do e.g. "Debate the chicken or the egg with the other AI"
    model: str # optional, model to use for this specific agent, if not provided use default

AgentDetails = tuple[Agent, Agent]