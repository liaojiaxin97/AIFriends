from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_toekn')
            if not refresh_token:
                return Response({
                    "result": "refresh_token不存在"
                },status=401)
            
            refresh = RefreshToken(refresh_token) #检测refreshtoken是否过期
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:     #如果开启了刷新token旋转，那么每次刷新都会生成一个新的refresh_token，
               refresh.set_jti()
               response = Response({
                     "result": "刷新成功",
                     'access': str(refresh.access_token),
               })
               #cookie中 是refresh
               response.set_cookie(
                    key = 'refresh_toekn',
                    value = str(refresh),
                    httponly = True,
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
               )
               return response
            #如果不需要刷新，则直接返回，返回到前端的是access
            response = Response({
                "result": "刷新成功",
                'access': str(refresh.access_token),
            })
        except:
            return Response({
                "result": "refresh_token过期了"
            }, status=401)