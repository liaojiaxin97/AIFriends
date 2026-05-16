import os
from datetime import datetime
import pprint
from typing import Annotated, Sequence, TypedDict
import lancedb
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from openai import OpenAI
from web.documents.utils.custom_embedding import CustomEmbeddings
from langchain_community.vectorstores import LanceDB

class ChatGraph:
    @staticmethod
    def create_app():
        @tool
        def get_time() -> str:
            '''获取当前时间的工具函数,返回格式为：[年-月-日 时:分:秒]'''
            
            return datetime.now().strftime("%Y-%m %H:%M:%S")
        
        @tool
        def search_knowledge(query:str) -> str:
            '''当用户查询阿里云百炼平台的相关信息时，调用此函数，输入要查询的问题，输出为查询结束'''
            db = lancedb.connect('./web/documents/lancedb_storage')
            embeddings = CustomEmbeddings()
            vector_db = LanceDB(
                connection = db,                
                embedding = embeddings,
                table_name = 'my_knowledge_base',

            )
            docs = vector_db.similarity_search(query,k=3)
            context = '\n\n'.join([f'内容片段：{i + 1}\n {doc.page_content}' for i, doc in enumerate(docs)])
            return f'从知识库中找到以下相关信息：\n\n{context}\n'
        tools = [get_time,search_knowledge]
        
        
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
        ).bind_tools(tools)
        
        #通过 AgentState 定义图里要传递的数据结构，这里只有 messages
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]
        # 作为图节点的执行逻辑
        def model_call(state: AgentState) -> AgentState:
            #pprint.pprint(state)
            res = llm.invoke(state['messages'])
            return {'messages':[res]}
        
        #检测是否有工具调用的节点，决定下一步走工具节点还是结束节点
        def should_continue(state:AgentState) -> str:
            last_message = state['messages'][-1]
            if last_message.tool_calls:
                return "tools"
            return "end"
        
        tool_node = ToolNode(tools)
        
        graph = StateGraph(AgentState)
        
        graph.add_node('agent',model_call)
        graph.add_node('tools',tool_node)
        
        graph.add_edge(START,'agent')
        graph.add_conditional_edges(
            'agent',
            should_continue,
            {
                'tools':'tools',
                'end':END
            }
            
        )
        graph.add_edge('tools','agent')
        
        return graph.compile()
    

