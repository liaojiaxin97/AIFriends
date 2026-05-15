import os
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages, StateGraph, START, END

class ChatGraph:
    @staticmethod
    def create_app():
        llm = ChatOpenAI(
            model = "deepseek-v4-flash",
            openai_api_key = os.getenv('API_KEY'),
            openai_api_base = os.getenv('API_BASE'),
            streaming = True,
            model_kwargs={
                "stream_options": {
                    "include_usage": True
                }
            }
        )
        
        #通过 AgentState 定义图里要传递的数据结构，这里只有 messages
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]
        # 作为图节点的执行逻辑
        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])
            return {'messages':[res]}
            
        graph = StateGraph(AgentState)
        
        graph.add_node('agent',model_call)
        
        graph.add_edge(START,'agent')
        graph.add_edge('agent',END)
        
        return graph.compile()
    

