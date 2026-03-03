#处理存储每个用户和虚拟角色的好友关系
from django.db import models
from web.models.user import UserProfile
from web.models.character import Character
from django.utils.timezone import now,localtime
class Friend(models.Model):
     #CASCADE：当Character被删除时，相关的关系也会被删除
    me = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    memory = models.TextField(default="",max_length = 5000,blank=True,null=True)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.character.name} - {self.me.user.username} - {localtime(self.create_time).strftime("%Y-%m-%d %H:%M:%S")}"
