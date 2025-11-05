
import json
from langchain_core.messages import ToolMessage
from my_agent.utils.tools import tools_by_name
from my_agent.utils.state import state_01


def tool_node_01(state: state_01):
    """Execute all tool calls from the last message in the state."""
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}
    


    

