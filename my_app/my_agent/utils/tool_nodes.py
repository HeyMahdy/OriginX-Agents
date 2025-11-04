from my_agent.utils.state import state_01
from my_agent.utils.tools import tools_by_name



def tool_node_01(state):
    outputs = []
    for call_tool in state["messages"][-1].tool_calls:
        if call_tool["name"] == "get_product_movements":
            result_01 = tools_by_name[call_tool["name"].invoke(call_tool[state["productId"]])]

    outputs.append(ToolMessage(
            content=json.dumps(tool_result),
            name=tool_call["name"],
            tool_call_id=tool_call["id"]
        ))


    

