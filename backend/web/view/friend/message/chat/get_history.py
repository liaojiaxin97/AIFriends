from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend, Message

class GetHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # try:
            last_message_id = int(request.query_params.get('last_message_id'))
            friend_id = request.query_params.get('friend_id')
            queryset = Message.objects.filter(friend_id = friend_id, friend__me__user = request.user)

            if last_message_id > 0:
                queryset = queryset.filter(id__lt = last_message_id)
            #因为上面取完是正序的，所以这里倒序一下，保证前端展示是按照时间顺序的
            messages_raw = queryset.order_by('-id')[:1]
            messages = []
            
            for m in messages_raw:
                messages.append({
                    'id':m.id,
                    'user_message':m.user_message,
                    'output':m.output,
                })
            return Response({
                'result':'success',
                'message':messages,
            })
        # except:
        #     return Response({
        #         'result':'error',
        #     })