
from my_app.main import app
from my_agent.utils.prompts import system_message_01, system_message
from my_agent.utils.tools import tools
from typing import Any
from my_agent.utils.state import state_01
_model_with_tools = None  # optional cache


def _get_llm():
    llm = getattr(app.state, "llm", None)
    if llm is None:
        raise RuntimeError("LLM not initialized yet; ensure FastAPI lifespan ran")
    return llm


def evidence_agent(state: state_01):
    global _model_with_tools
    if _model_with_tools is None:
        _model_with_tools = _get_llm().bind_tools(tools)

    model = system_message_01 | _model_with_tools
    response = model.invoke({"agent_scratchpad_01": state["messages"]})
    return {"messages": [response]}


def SupervisorAgent(state:state_01):
    llm = _get_llm()
    model = system_message | llm
    response = model.invoke({"agent_scratchpad": state["messages"]})
    return {"messages": [response]}
