from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from langchain_core.messages import HumanMessage

from web.models.friend import Friend, Message
from web.view.friend.message.chat.graph import ChatGraph

#因为此处是与大模型交互，报错较多，不进行try catch
class MessageView(APIView):
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
        res = app.invoke(inputs)
        
        print(res['messages'][-1].content)
        
        return Response({
            'result':'success',
        })