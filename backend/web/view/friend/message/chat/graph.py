import os
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages, StateGraph, START, END



class ChatGraph:
    @staticmethod
    def create_app():
        #连接大模型
        llm = ChatOpenAI(
            model="deepseek-v3.2",
            openai_api_key=os.getenv("API_KEY"),
            openai_api_base=os.getenv("API_BASE"),
            streaming=True,
            model_kwargs={
                "stream_options": {
                    "include_usage":True,  #输出token数量
            }
            }
        )
        #定义状态类型，包含消息列表
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]
            
        #agent逻辑，接收状态，调用大模型获取回复，返回新的状态 
        def model_call(state: AgentState) -> AgentState:
            #调用大模型，传入消息列表，获取回复
            res = llm.invoke(state['messages'])
            #将回复添加到消息列表中
            return {'messages':[res]}
        
        graph = StateGraph(AgentState)
        graph.add_node('agent',model_call)
        graph.add_edge(START,'agent')
        graph.add_edge('agent',END)
        
        return graph.compile()