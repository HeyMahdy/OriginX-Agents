# workflow.py
from ...main import app 
from my_agent.utils.prompts import system_message_01
from my_agent.utils.tool_nodes import tool_node_01
from langgraph.graph import StateGraph, START, END
from my_agent.utils.agent import evidence_agent , SupervisorAgent
# Initialize the graph immediately on import
workflow = StateGraph(state)

workflow.add_node("SupervisorAgent", SupervisorAgent)
workflow.add_node("evidence_agent", evidence_agent)
workflow.add_node("tool_node", tool_node_01)




def should_continue_01(state):
    last_message = state["messages"][-1]
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "tools"
    else :
        return "next_agent"
    


workflow.add_conditional_edges(
    "evidence_agent",
    should_continue_01,
    {
        "tool_node":"tool_node",
          "END": END
    }
)

workflow.add_conditional_edges(
    "SupervisorAgent",
    should_continue_01,
    {
        "evidence_agent":"evidence_agent"
    }
)