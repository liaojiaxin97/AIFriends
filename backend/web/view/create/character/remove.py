from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character
from web.models.user import UserProfile

from web.view.utils.photo import remove_old_photo

#删除时，头像和背景一并删掉
class RemoveCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            character_id = request.data['character_id']
            #get 和filer 区别，前者返回一个元素，后者返回数组
            character = Character.objects.get(pk = character_id, author__user = request.user)
            remove_old_photo(character.photo)
            remove_old_photo(character.background_image)
            character.delete()
            return Response({
                'result':'success',
            })
        except:
            return Response({
                'result':'系统异常，请稍后重试'
            })