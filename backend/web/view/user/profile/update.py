from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from web.models.user import UserProfile
from web.view.utils.photo import remove_old_photo

from django.contrib.auth.models import User
from django.utils.timezone import now

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            user = request.user
            #只匹配一个用户，get方法，如果匹配不到或者匹配到多个都会抛异常
            user_profile = UserProfile.objects.get(user=user)
            username = request.data.get('username').strip()
            profile = request.data.get('profile').strip()[:500] #简介限制500字
            photo = request.FILES.get('photo',None)
            #防止恶意用户 发送请求
            if not username:
                return Response({'result':'用户名不能为空'})
            if not profile:
                return Response({'result':'简介不能为空'})
            
            if username != user.username and User.objects.filter(username=username).exists():
                return Response({'result':'用户名已存在'})
            if photo:
                remove_old_photo(user_profile.photo)
                user_profile.photo = photo
            user_profile.profile = profile
            user_profile.update_time = now()
            user_profile.save()
            user.username = username
            user.save()
            return Response({
                'result': 'success',
                'use_id': user.id,
                'username': user.username,
                'profile': user_profile.profile,
                'photo': user_profile.photo.url,
            })
        except:
            return Response({'result':'系统异常，请稍后再试'})