
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.view.utils.photo import remove_old_photo
from web.models.character import Character
from django.utils.timezone import now

class UpdateCharacterView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self,request):
        try:
            character_id = request.data['character_id']
            character = Character.objects.get(id = character_id, author__user = request.uer)
            name = request.data['name'].strip()
            profile = request.data['profile'].strip()[:100000]
            photo = request.FILES('photo',None)
            background_image = request.FILES.get('background',None)

            if not name:
                return Response({
                    'result':'名字不能为空'
                })
            if not profile:
                return Response({
                    'result':'用户简介不能为空'
                })
            if photo:
                remove_old_photo(character.photo)
                character.photo = photo
            
            if background_image:
                remove_old_photo(character.background_image)
                character.background_image = background_image
            
            character.name = name
            character.profile = profile
            character.update_time = now()
                
        except:
            Response({
                'result':'系统异常，请重试'
            })
        