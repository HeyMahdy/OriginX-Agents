

from my_agent.utils.prompts import system_message_01, system_message
from my_agent.utils.tools import tools
from typing import Any
from my_agent.utils.state import state_01
from my_agent.utils.llm_store import get_llm as _get_llm

_model_with_tools = None  # optional cache


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
