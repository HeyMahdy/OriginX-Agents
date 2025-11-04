from ...main import app 
from my_agent.utils.prompts import system_message_01 , system_message
from my_agent.utils.tools import tools


model_react_01=system_message_01|app.state.llm.bind_tools(tools)
def evidence_agent(state):
    response = model_react_01.invoke({"agent_scratchpad_01": state["messages"]})
    return {
        "messages": [response]
    }

model_react = system_message | app.state.llm
def SupervisorAgent(state):
    response = model_react.invoke({"agent_scratchpad": state["messages"]})
    return {
        "messages": [response]
    }