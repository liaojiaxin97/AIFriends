from django.urls import path
from web.view.index import index    
from web.view.user.account.login import LoginView
from web.view.user.account.register import RegisterView
from web.view.user.account.logout import LogoutView
from web.view.user.account.refresh_toekn import RefreshTokenView
from web.view.user.account.get_user_info import GetUserInfoView
urlpatterns = [
    #后端前面不用加/
    #要用api开头，区分前后端路由，不然后跟前端路由冲突了
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    
    path('api/user/account/get_user_info/', GetUserInfoView.as_view()),
    
    path("", index, name='index')
]
