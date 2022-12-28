from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(ShopingCart)
admin.site.register(Conversation)
admin.site.register(Chat)
admin.site.register(Group)
admin.site.register(GroupUsers)
admin.site.register(GroupChat)
admin.site.register(VideoChat)
admin.site.register(VideoChatUsers)