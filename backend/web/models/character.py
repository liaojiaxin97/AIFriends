from django.db import models
import uuid
from django.utils.timezone import now, localtime

from web.models.user import UserProfile

def photo_upload_to(instance,filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/photos/{instance.author.user_id}_{filename}'


def background_upload_to(instance,filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/background_images/{instance.author.user_id}_{filename}'

class Character(models.Model):
    #外键
    author = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    photo = models.ImageField(upload_to=photo_upload_to)
    profile = models.TextField(max_length=100000)
    background_image = models.ImageField(upload_to = background_upload_to)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)
    #创建完数据库后，在对应  admin  中注册Character模型，并设置raw_id_fields = ('author', )，以便在admin界面中选择外键时使用原始ID输入框。
    def __str__(self):
        return f'{self.author.user.username} - {self.name} - {localtime(self.create_time).strftime("%Y-%m-%d %H:%M:%S")}'