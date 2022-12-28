from datetime import datetime
import json
from time import timezone
from tokenize import group
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.humanize.templatetags.humanize import naturaltime
from Buyer.models import Conversation,Chat,User
from django.db.models import Q,Avg
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
import asyncio 
from django.utils import timezone as tz
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from Accounts .models import User
from django.template.loader import render_to_string

from Buyer.models import GroupChat as gc,Group,GroupUsers
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_with = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope["user"]
        self.conv_id=Conversation.objects.filter(Q(seller=self.user,buyer__chat_name=self.chat_with) |Q(buyer=self.user,seller__chat_name=self.chat_with)).first()
        self.room_group_name = str(self.conv_id.conversation_id)
      
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat,created=Chat.objects.get_or_create(sender=self.user,conversation_id=self.conv_id,message=message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'reciver':self.chat_with,
                'sender':self.user.id,
                'chat_id':chat.id,
                'date_time':str((chat.date).strftime("%Y-%m-%d %H:%M:%S"))
            }
        )
   
    # Receive message from room group
    def chat_message(self, event):
        
        message = event['message']
        reciver = event['reciver']
        sender = event['sender']
        chat_id=event['chat_id']
        date_time=event['date_time']
        chat=Chat.objects.get(id=chat_id)
        
        date=datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
        
        natural=naturaltime(date)
       
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'status':chat.status,
            'sender':sender,
            'date_time':str(natural)
          
           
        }))
    
class GroupChat(WebsocketConsumer):
    def connect(self):
        self.chat_with = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope["user"]
        print(self.chat_with)
        self.group=Group.objects.filter(group_id=self.chat_with).first()
        self.room_group_name = str(self.group.group_id)
        self.group_user=GroupUsers.objects.filter(user=self.user,group=self.group).first()
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat,created=gc.objects.get_or_create(sender=self.group_user,group=self.group,message=message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender':self.user.id,
                'chat_id':chat.id,
                'status':chat.status,
                'date_time':str(chat.get_human_time())
            }
        )
   
    # Receive message from room group
    def chat_message(self, event):
        
        message = event['message']
        sender = event['sender']
        
        date_time=event['date_time']
        status=event['status']
        
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'status':status,
            'sender':sender,
            'date_time':date_time
          
           
        }))
class Notification(WebsocketConsumer):
    def connect(self):
        self.notificationid = self.scope['url_route']['kwargs']['room_name']
        self.notificationid=str(self.notificationid)
        async_to_sync(self.channel_layer.group_add)(
            self.notificationid,
            self.channel_name
        )

        self.accept()
        self.user=User.objects.filter(notification_id=str(self.notificationid)).first()
        if self.user.is_authenticated:
            self.user.status="Online"
            self.user.save()	
        self.send_status()
        #find chats
        conversations=Chat.objects.filter(Q(conversation_id__seller=self.user) | Q(conversation_id__buyer=self.user),~Q(sender=self.user),status="Pending")
        if len(conversations)>0:
            for msg in conversations:
                data={"current":msg.message,"sender":msg.sender.chat_name}
                async_to_sync(self.channel_layer.group_send)(
                self.notificationid,{
                    "type":"send_notification",
                    "value":json.dumps(data),
                }
                )
                msg.status="Delivered"
                msg.save()
       
    
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.notificationid,
            self.channel_name
        )
        if self.user:
            self.user.status="Offline"
            self.user.last_seen=tz.now()
            self.user.save()
        self.send_status()

    def send_status(self):
        conversations=Conversation.objects.filter(Q(seller=self.user) | Q(buyer=self.user)).distinct()
        last_seen=str(naturaltime(self.user.last_seen))
        data={"user":self.user.email,"online_chat_name":self.user.chat_name,"id":self.user.id,"user_status":str(self.user.status).lower(),"last_seen":last_seen}
        for con in conversations:
            send_to=None
            if con.seller==self.user:
                send_to=con.buyer
            else:
                send_to=con.seller
            async_to_sync(self.channel_layer.group_send)(
                    str(send_to.notification_id),{
                        "type":"send_notification",
                        "value":json.dumps(data),
                    }
                    ) 
    def send_notification(self,event):
        tem=json.loads(event["value"])
        data=event["value"]
        try:
            if self.user.status=="Online":
                messageid=tem['mid']
                ch=Chat.objects.filter(id=messageid).first()
                if ch:
                    ch.status="Delivered"
                    ch.save()
        except Exception as ex:
            pass
        self.send(text_data=event["value"])
    def send__group_notification(self,event):
        
        self.send(text_data=event["value"])
        
   
