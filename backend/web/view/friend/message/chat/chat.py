import json
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
from langchain_core.messages import HumanMessage, BaseMessageChunk

from web.models.friend import Friend, Message
from web.view.friend.message.chat.graph import ChatGraph

#渲染器，防止DRF报错
class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


#因为此处是与大模型交互，报错较多，不进行try catch
class MessageView(APIView):
    renderer_classes = [SSERenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        friend_id = request.data['friend_id']
        message = request.data['message'].strip()
        if not message:
            return Response({"result":"消息不能为空"})
        #筛选主键等于 friend_id 且通过关系 me 的 user 字段等于当前用户的 Friend 记录。
        #pk就是id
        friends = Friend.objects.filter(pk = friend_id, me__user = request.user)
        if not friends.exists():
            return Response({"result":"好友关系不存在"})
        friend = friends.first()
        
        app = ChatGraph.create_app()
        
        inputs = {
            'messages': [HumanMessage(message)]
        }
        # #非流式
        # res = app.invoke(inputs)
        
        #后端流式实现：定义一个生成器函数，使用yield关键字逐步返回数据块，每次调用yield时，函数会暂停执行并返回当前的数据块，直到下一次调用时继续执行。
        
        #定义生成器
        #SSE模式：服务器发送事件（Server-Sent Events），是一种单向通信协议，服务器可以持续向客户端推送数据，而客户端只能接收数据，不能向服务器发送数据。
        def event_stream():
            full_output = ''
            full_usage = {}
            for msg,metadata in app.stream(inputs,stream_mode = "messages"):
                if isinstance(msg, BaseMessageChunk):
                    if msg.content:
                        full_output += msg.content
                        #每次调用，执行一次yield，返回一个消息块给前端，前端可以实时显示
                        #如果没有消息可以yield,报错"Generator didn't yield anything"
                        yield f'data:{json.dumps({"content":msg.content},ensure_ascii=False)}\n\n'
                    if hasattr(msg,'usage_metadata') and msg.usage_metadata:
                        full_usage = msg.usage_metadata
            yield 'data:[DONE]\n\n'
            #存取消耗的token
            input_tokens = full_usage.get('input_tokens',0)
            output_tokens = full_usage.get('output_tokens',0)
            total_tokens = full_usage.get('total_tokens',0)
            Message.objects.create(
                friend = friend,
                user_message = message[:500],
                input = json.dumps(
                   [m.model_dump() for m in inputs['messages']],
                   ensure_ascii=False,
                ),
                output = full_output[:500],
                input_tokens = input_tokens,
                output_tokens = output_tokens,
                total_tokens = total_tokens
            )
            print(full_usage)
        
        #自动用next迭代生成器---测试用例
        # for data in event_stream():
        #     print(data)
        
        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        #清除缓存
        response['Cache-Control'] = 'no-cache'
        return response
        