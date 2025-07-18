from a2a.types import AgentCard, AgentCapabilities, AgentSkill

hello_skill = AgentSkill(
    id="echo",
    name="Echo Skill",
    description="Echoes the input.",
    tags=["echo", "simple"],
    examples=["PING!"],
)

agent_card = AgentCard(
    name="SimpleEchoAgent",
    description="An agent that echoes input.",
    version="1.0.0",
    url="http://localhost:9999/",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[hello_skill],
)
