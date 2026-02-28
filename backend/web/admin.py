from django.contrib import admin

# Register your models here.
from web.models.user import UserProfile

from web.models.friend import Friend
##数据库创建
from web.models.character import Character
@admin.register(UserProfile)

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )  #
    
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', )
@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    #外键加载
    #不写的话会加载所有角色，如果很多会卡
    raw_id_fields = ('me','character',)
###注册完成后，使用python .\manage.py makemigrations
#python manage.py makemigrations：生成数据库更新操作
#python manage.py migrate：将数据库的更新同步到db.sqlite3（或者其他数据库，例如mysql）中