from django.contrib import admin

# Register your models here.
from web.models.user import UserProfile

@admin.register(UserProfile)

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )  #保证传入的是字典