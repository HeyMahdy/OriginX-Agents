from typing import Annotated
from typing_extensions import TypedDict


from typing import Optional, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from operator import add


class state_01(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    productId: str                
    reason: str                      
    reporterId: str                  
    orgId: str                      
    purchaseDate: str
    token: str

