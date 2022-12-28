from itertools import product
import json
from tokenize import group
from django.db import models
from django.utils import timezone
# Create your models here.
from django.core.exceptions import ValidationError
import uuid
import string
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from Accounts.models import User
from Seller.models import *
import random
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
class ShopingCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    qty=models.IntegerField(default=1)
    def __str__(self) -> str:
        return f"{self.user} save {self.product} in cart and qty is {self.qty}"
def get_unique():
    return str(dt.datetime.now())+str(uuid.uuid4().hex[:10].upper())+str(randint(0,10000))
    
class ProductComments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    comment=models.CharField(max_length=150)
    comment_at=models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.user} comment on {self.product} comment is {self.comment} at {self.comment_at}"
    

    
class Group(models.Model):
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    group_name=models.CharField(max_length=20,unique=True)
    group_id=models.UUIDField(default=uuid.uuid4(),editable=False)
    date_time=models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.group_name
    def group_users(self):
        users=GroupUsers.objects.filter(group=self)
        return users
    def count_users(self):
        return len(self.group_users())
    def get_admins(self):
        users=GroupUsers.objects.filter(group=self,is_admin=True)
        
        return users
    def get_users_statues(self):
        online=GroupUsers.objects.filter(group=self,user__status="Online")
        offline=GroupUsers.objects.filter(group=self,user__status="Offline")
        return [online.count(),offline.count(),online,offline]
message_status=(
    ("Pending","Pending"),
    ("Delivered","Delivered"),
    ("read","read"),
)
class GroupUsers(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False)
    date_time=models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return f'{self.group} {self.user}'
class GroupChat(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    sender=models.ForeignKey(GroupUsers,on_delete=models.CASCADE)
    message=models.CharField(max_length=255)
    date_time=models.DateTimeField(default=timezone.now)
    status=models.CharField(choices=message_status,default="Pending",max_length=30)
    
    def __str__(self) -> str:
        return self.message
    def get_human_time(self):
        return naturaltime(self.date_time)
    
    def sender_is_admin(self):
        return self.sender.is_admin
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status=="Pending":
            notification_id=None
            groupusers=GroupUsers.objects.filter(group=self.group)
            
            for user in groupusers:
                if user != self.sender:
                    notification_id=str(user.user.notification_id)
                    channel_layer=get_channel_layer()
                    
                    data={"current":self.message,"sender":self.group.group_name,"mid":self.id}
                    async_to_sync(channel_layer.group_send)(
                        notification_id,{
                            "type":"send__group_notification",
                            "value":json.dumps(data),
                        }
                    )
                """self.status="Delivered"
                self.save()"""
    
class Conversation(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Buyer")
    seller=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Seller")
    conversation_id=models.UUIDField(default=uuid.uuid4(),editable=False)
    date=models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        if self.conversation_id:
            return str(self.conversation_id)
        else:
            return f"Seller:{self.seller} buyer:{self.buyer}"
    def save(self,*args, **kwargs):
        if self.buyer != self.seller:
            return super().save(*args, **kwargs)
        else:
            raise ValidationError({"sender":"You cannot chat with itself"})
        
    def get_unread_chat(self):
        messages=Chat.objects.filter((Q(status="Pending" )| Q(status="Delivered")),conversation_id=self)
        return messages
def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str
    
class VideoChat(models.Model):
    code=models.CharField(default=get_random_string,unique=True,max_length=10)
    chat_id=models.UUIDField(default=uuid.uuid4(),unique=True)
    created_at=models.DateTimeField(default=timezone.now)
    id_valid=models.BooleanField(default=True)
    
    
class VideoChatUsers(models.Model):
    video_chat=models.ForeignKey(VideoChat,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False)
    
class Chat(models.Model):
    conversation_id=models.ForeignKey(Conversation,on_delete=models.CASCADE,default=None)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.CharField(max_length=255)
    status=models.CharField(choices=message_status,default="Pending",max_length=30)
    date=models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return f'{self.sender} status:{self.status}'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status=="Pending":
            notification_id=None
            other=self.conversation_id.buyer
            if self.sender==other:
                notification_id=self.conversation_id.seller.notification_id
            else:
                notification_id=other.notification_id
            count=Chat.objects.filter( Q(conversation_id__seller=other) | Q(conversation_id__buyer=other),status="Pending").count()
            
            notification_id=str(notification_id)
            channel_layer=get_channel_layer()
            
            data={"current":self.message,"sender":self.sender.chat_name,"count":count,"mid":self.id,'uid':self.sender.id}
            async_to_sync(channel_layer.group_send)(
                notification_id,{
                    "type":"send_notification",
                    "value":json.dumps(data),
                }
            )
            """self.status="Delivered"
            self.save()"""
    
