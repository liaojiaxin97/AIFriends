import json

from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from langchain_core.messages import BaseMessageChunk, HumanMessage

from rest_framework.renderers import BaseRenderer
from web.models.friend import Friend, Message
from web.view.friend.message.chat.graph import ChatGraph

class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
    
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
        
        response = StreamingHttpResponse(event_stream(),content_type = "text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response
        