from django.urls import path, re_path
from web.view.index import index    
from web.view.user.account.login import LoginView
from web.view.user.account.register import RegisterView
from web.view.user.account.logout import LogoutView
from web.view.user.account.refresh_toekn import RefreshTokenView
from web.view.user.account.get_user_info import GetUserInfoView
from web.view.user.profile.update import UpdateProfileView

urlpatterns = [
    #后端前面不用加/
    #要用api开头，区分前后端路由，不然后跟前端路由冲突了
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    
    path('api/user/account/get_user_info/', GetUserInfoView.as_view()),
    path('api/user/profile/update/', UpdateProfileView.as_view()),
    
    path("", index, name='index'),

    #兜底路由
    # 其他路径都交给前端路由处理，除了media、static、assets这些静态资源路径
    # 匹配所有不以静态文件路径开头的URL，并将其交给index视图处理
    # 这样可以确保前端路由能够正确处理除静态资源以外的所有请求
    # 使得前端路由根据路径展示不同的页
    # 示例 ---》返回index.html（前端vue-->app.vue-->routerView-->router/index.js找到对应的页面），
    
    re_path(r'^(?!media/|static/|assets/).*$', index),
]
