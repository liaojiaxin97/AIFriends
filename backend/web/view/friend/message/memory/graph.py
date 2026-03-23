import os
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages, StateGraph, START, END
from typing import Annotated, Sequence, TypedDict


#记忆模块不返回消息，单纯调用大模型进行记忆更新，因此不需要工具节点和状态转移条件
class MemoryGraph:
    @staticmethod
    def create_app():
        llm = ChatOpenAI(
            model="deepseek-v3.2",
            openai_api_key=os.getenv("API_KEY"),
            openai_api_base=os.getenv("API_BASE"),
        )
        
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]
        
        def model_call(state: AgentState) -> AgentState:
            # print(state)
            res = llm.invoke(state['messages'])
            return {'messages':[res]}
        
        graph = StateGraph(AgentState)
        
        graph.add_node('agent',model_call)
        graph.add_edge(START,'agent')
        graph.add_edge('agent',END)
        return graph.compile()