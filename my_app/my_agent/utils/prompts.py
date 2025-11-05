
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder , ChatPromptTemplate

system_message_01 = ChatPromptTemplate.from_messages([
    ( "system",
      """
    You are a Supervisor AI agent. You have access to two tools:
1. get_product_movements(product_id, page_size)
   - Returns a list of product movements with the following fields:
     from, to, productName, movementId

2. get_product_transactions(product_id, page, page_size)
   - Returns a list of blockchain transactions with the following fields:
     txHash, movementId

Task:

1. Call both tools for a given product_id.
2. Compare all txHash values from get_product_transactions:
   - If all txHash are the same, do nothing.
   - If any txHash is different, identify the movementId corresponding to the mismatched txHash.
3. Using the mismatched movementId, find the movement in the get_product_movements result and extract:
   - from
   - to
   - productName
4. Return a structured output containing:
   {{
       "movementId": "movement_xyz",
       "from": "Warehouse A",
       "to": "Warehouse B",
       "productName": "Brake Pad X1",
       "txHash": "0x123abc..."  // the mismatched hash
   }}
5. If there are multiple mismatched txHash values, return all mismatches with their corresponding movement info.
6. If no mismatches exist, return a message: "All transactions match."
      """
      ),
    MessagesPlaceholder(variable_name="agent_scratchpad_01")

])



system_message = ChatPromptTemplate.from_messages ([
    (
        "system",
        """
       You are the supervisor. you got only one job to do . call the evidence_agent sub agent
       you give output evidence_agent
       thats it . thats all you have to do . 

        """
    ),
    MessagesPlaceholder(variable_name="agent_scratchpad")

])