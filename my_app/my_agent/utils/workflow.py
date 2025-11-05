# workflow.py
from my_agent.utils.prompts import system_message_01
from my_agent.utils.tool_nodes import tool_node_01
from langgraph.graph import StateGraph, START, END
from my_agent.utils.agent import evidence_agent , SupervisorAgent
from my_agent.utils.state import state_01
# Initialize the graph immediately on import

workflow = StateGraph(state_01)

workflow.add_node("SupervisorAgent", SupervisorAgent)
workflow.add_node("evidence_agent", evidence_agent)
workflow.add_node("tool_node", tool_node_01)


def route_from_supervisor(state: state_01):
    messages = state["messages"]
    last_message = messages[-1]
    return "tools" if getattr(last_message, "tool_calls", None) else "evidence"


def route_from_evidence(state: state_01):
    messages = state["messages"]
    last_message = messages[-1]
    return "tools" if getattr(last_message, "tool_calls", None) else "end"


# Wire graph
workflow.add_edge(START, "SupervisorAgent")
workflow.add_conditional_edges(
    "SupervisorAgent",
    route_from_supervisor,
    {
        "tools": "tool_node",
        "evidence": "evidence_agent",
    },
)
workflow.add_conditional_edges(
    "evidence_agent",
    route_from_evidence,
    {
        "tools": "tool_node",
        "end": END,
    },
)

# After tools, go back to evidence agent to let the model observe results
workflow.add_edge("tool_node", "evidence_agent")

# Compile a runnable graph
graph = workflow.compile()