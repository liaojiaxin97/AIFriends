#返回个人主页的两个内容-用户信息和角色列表-
#无需登录

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from web.models.user import UserProfile
from web.models.character import Character



class GetListCharacterView(APIView):
    def get(self, request):
        try:
            #传给后端，前端已经有多少内容
            #需要转换字符串为整数
            items_count= int(request.query_params.get('items_count'))
            #确定当前空间是哪个user的
            user_id = request.query_params.get('user_id')  #返回字符串
            user = User.objects.get(id = user_id)  #查询对应user时自动讲user_id转换为int类型
            user_profile = UserProfile.objects.get(user=user)
            characters_raw = Character.objects.filter(
                author = user_profile
                ).order_by('-id')[items_count: items_count + 20]   #按照创建时间倒序排序（id递增，加减号倒序）
            
            characters = []

            for character in characters_raw:
                author = character.author
                characters.append({
                    'id':character.id,
                    'name':character.name,
                    'profile':character.profile,
                    'photo':character.photo.url,
                    'background_image':character.background_image.url,
                    'author':{
                        'user_id':author.user_id,
                        'username':author.user.username,
                        'photo':author.photo.url,
                    }
                })
            return Response({
                'result':'success',
                'user_profile':{
                    'user_id':user.id,
                    'username':user.username,
                    'profile':user_profile.profile,
                    'photo':user_profile.photo.url,
                },        
                'characters':characters,
            })
        except:
            return Response({
                'result':'系统异常，请稍后重试'
            })