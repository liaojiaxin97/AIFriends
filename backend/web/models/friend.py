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

#存储聊天信息
class Message(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    #用户输入
    user_message = models.TextField(max_length = 500)
    #大模型自己的prompt
    input = models.TextField(max_length=5000)
    output = models.TextField(max_length=5000)
    
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=now)
    #消耗token数量

    def __str__(self):
        return f"{self.friend.character.name} - {self.friend.me.user.username} - {self.user_message[:50]} - {localtime(self.create_time).strftime("%Y-%m-%d %H:%M:%S")}"