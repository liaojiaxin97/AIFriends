import os
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from datetime import datetime
import pprint
from rest_framework.response import Response
import lancedb
from web.documents.utils.custom_embeddings import CustomEmbeddings
from langchain_community.vectorstores import LanceDB
import pprint as pprint

class ChatGraph:
    @staticmethod
    def create_app():
        
        @tool
        def get_time() -> str:
            '''当需要查询精确时间时，调用此函数，返回格式为：[年-月-日 时：分：秒]'''
  
            return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

        @tool
        def search_knowledge_base(query:str) -> str:
            '''当用户查询阿里云百炼平台相关信息时，调用此函数，输入要查询的问题，输出为查询结果'''
            db = lancedb.connect('./web/documents/lancedb_storage')
            embeddings = CustomEmbeddings()
            vector_db = LanceDB(
                connection=db,
                embedding=embeddings,
                table_name='my_knowledge_base',
            )
            docs = vector_db.similarity_search(query, k=3)
            context = '\n\n'.join([f'内容片段:{i+1}\n{doc.page_content}' for i, doc in enumerate(docs)])
            return f'从知识库中找到以下信息：\n\n{context}\n'
        tools = [get_time,search_knowledge_base]
            
        
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
        ).bind_tools(tools)
        #定义状态类型，包含消息列表
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]
            
        #agent逻辑，接收状态，调用大模型获取回复，返回新的状态 
        def model_call(state: AgentState) -> AgentState:
            # pprint.pprint(state['messages'])
            #调用大模型，传入消息列表，获取回复
            res = llm.invoke(state['messages'])
            #将回复添加到消息列表中
            return {'messages':[res]}
        #定义状态转移条件，根据大模型回复的内容，判断下一步是调用工具还是结束
        def should_continue(state: AgentState) -> str:
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                return "tools"
            return "end"
        #创建工具节点
        tool_node = ToolNode(tools)
        
        graph = StateGraph(AgentState)
        graph.add_node('agent',model_call)
        graph.add_node('tools',tool_node)
        graph.add_edge(START,'agent')
        graph.add_conditional_edges(
            'agent',
            should_continue,
            #自动路由到对应节点
             {
                 "tools":"tools",
                 "end":END,
             }
        )
        graph.add_edge('tools','agent')
        
        
        return graph.compile()