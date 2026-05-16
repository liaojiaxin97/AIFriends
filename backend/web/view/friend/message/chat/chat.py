import json
import pprint

from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from langchain_core.messages import AIMessage, BaseMessageChunk, HumanMessage, SystemMessage

from rest_framework.renderers import BaseRenderer
from web.view.friend.message.memory.update import update_memory
from web.models.friend import Friend, Message
from web.view.friend.message.chat.graph import ChatGraph
from web.models.friend import SystemPrompt
class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


#添加系统提示词
def add_system_prompt(state,friend):
    msgs = state['messages']
    system_prompts= SystemPrompt.objects.filter(title = "回复").order_by('order_number')
    prompt = ''
    
    for sp in system_prompts:
        prompt += sp.prompt
    prompt += f'\n【角色性格】\n {friend.character.profile}\n'
    prompt += f'【长期记忆】\n{friend.memory}\n'
    return {'messages':[SystemMessage(prompt)] + msgs}


#添加最近十轮对话

def add_recent_messages(state,friend):
    msgs = state['messages']
    message_raw = list(Message.objects.filter(friend = friend).order_by('-id')[:10])
    message_raw.reverse()
    messages = []
    for m in message_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))
    return {'messages':msgs[:1] + messages + msgs[-1:]}


class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]
    def post(self, request):
        friend_id = request.data['friend_id']
        message = request.data['message'].strip()
        # print(friend_id, message)
        if not message:
            return Response({'error': '消息不能为空'}, status=400)
        #从friend中查询数据
        #查询这个好友是否属于当前登录用户，第一个参数是查找当前对话框对应的朋友，第二个是确认当前对话框对应的朋友是已经登陆的用户的朋友
        friends = Friend.objects.filter(id = friend_id, me__user = request.user)
        
        if not friends.exists():
            return Response({'error': '好友不存在'})
        
        friend = friends.first()
        
        app = ChatGraph.create_app()
        
        inputs = {
            'messages':[HumanMessage(message)]
        }
        inputs = add_system_prompt(inputs,friend)
        inputs = add_recent_messages(inputs,friend)
        ### 系统提示词 + 最近十轮消息 + 用户最新的消息###
        ##pprint.pprint(inputs)
        #非流式发送和输出
        # res = app.invoke(inputs)
        # # print(res)
        # print(res['messages'][-1].content)
        
        #流式发送和输出
        def event_stream():
            full_output = ''
            full_usage = {}
            for msg,metadata in app.stream(inputs,stream_mode = "messages"):
                if isinstance(msg, BaseMessageChunk):
                    if msg.content:
                        full_output += msg.content
                        #将消息包装成前端需要的格式，发送给前端 --> data:{"content":"模型输出的一小段内容"}
                        yield f"data:{json.dumps({'content': msg.content}, ensure_ascii=False)}\n\n"
                    if hasattr(msg,'usage_metadata') and msg.usage_metadata:
                        full_usage = msg.usage_metadata
            yield 'data: [DONE]\n\n'
            ####  SSE固定格式 data:{"content":""}\n\n  data: [DONE]\n\n ####
            
            input_tokens = full_usage.get('input_tokens', 0)
            output_tokens = full_usage.get('output_tokens', 0)
            total_tokens = full_usage.get('total_tokens', 0)
            
            Message.objects.create(
                friend = friend,
                user_message = message,
                input = json.dumps(
                    [m.model_dump() for m in inputs['messages']],
                    ensure_ascii = False,
                ),
                
                output = full_output,
                input_tokens = input_tokens,
                output_tokens = output_tokens,
                total_tokens = total_tokens
            )
            
            
            # 输出结束，完整模型输出赢有了
            # print("完整的使用量统计:", full_usage)
            
        #模型流式输出样式
        # for data in event_stream():
        #     print(data)
        
            #每1条消息更新一次记忆
            #筛选出这个朋友的所有消息，并且返回这些消息的总数
            if Message.objects.filter(friend=friend).count() % 1 ==0:
                update_memory(friend)
            
            
        response = StreamingHttpResponse(event_stream(),content_type = "text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response
        