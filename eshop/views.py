from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from Seller.models import Store
from Seller.serializers import StoreSerializer
from Buyer.models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import constants as tags
# Create your views here.

MESSAGE_TAGS = {
    tags.INFO: 'info',
    tags.SUCCESS: 'success',
    tags.ERROR: 'error',
    
}
@login_required()
def home(request):
  if request.user.user_type=="Seller":
    store=request.session.get("store")
    if not store:
      store,created=Store.objects.get_or_create(store_owner=request.user)
      if not store.store_name:
        return redirect("store")
      data=StoreSerializer(store)
      data=data.data
      request.session["store"]=data
    return redirect("seller_home")
  else:
        return redirect("buyer_home")
@login_required()
def chat_home(request):
    
    conversations=Conversation.objects.filter(Q(seller=request.user) | Q(buyer=request.user)).distinct()
    groups=GroupUsers.objects.filter(user=request.user).distinct()
    return render(request, 'chat.html', {
        "conversations":conversations,
        "template":get_template(request.user.user_type),
        "groups":groups,
      
    })
@login_required()
def chat_with_user(request,chat_with):
  
  conversations=Conversation.objects.filter(Q(seller=request.user) | Q(buyer=request.user)).distinct()
  groups=GroupUsers.objects.filter(user=request.user).distinct()
  chat_with=User.objects.filter(chat_name=chat_with).first()
  if chat_with:
    conv_id=Conversation.objects.filter(Q(seller=chat_with,buyer=request.user)|Q(buyer=chat_with,seller=request.user)).first()
    if conv_id:
      messages=Chat.objects.filter(conversation_id=conv_id)
      for msg in messages:
        msg.status="read"
        msg.save()
        
      dict={"conv_id":conv_id,"chat_messages":messages,"conversations":conversations,
        "room_name":chat_with.chat_name,"chat_with":chat_with,
        "template":get_template(request.user.user_type),"groups":groups}
    else:
      seller=None
      buyer=None
      if chat_with.user_type=="Seller":
        seller=chat_with
        buyer=request.user
      else:
        seller=request.user
        buyer=chat_with
      conv_id=Conversation.objects.create(seller=seller,buyer=buyer)
      dict={"conv_id":conv_id,"messages":[],"conversations":conversations,
      "room_name":chat_with.chat_name,"chat_with":chat_with,
      "template":get_template(request.user.user_type),"groups":groups}
    return render(request,"chat.html",dict)
  else: 
    print("Error")
    
  return redirect("chat")
def chat_with_groups(request,chat_with):
  group_name=chat_with
  conversations=Conversation.objects.filter(Q(seller=request.user) | Q(buyer=request.user)).distinct()
  groups=GroupUsers.objects.filter(user=request.user).distinct()
  group=Group.objects.filter(group_name=group_name).first()
  group_user,created=GroupUsers.objects.get_or_create(user=request.user,group=group)
  if created:
    
    messages.info(request,f'Your are added in {group} group')
  if group:
    grp_chat=GroupChat.objects.filter(group=group)
    dict={"group_id":group.group_id,"group_messages":grp_chat,"conversations":conversations,
      "room_name":group.group_name,"chat_with":group,
      "template":get_template(request.user.user_type),"groups":groups,}
    return render(request,"chat_group.html",dict)
def get_template(type):
  temp="BuyerBase.html"
  if type=="Seller":
    temp="SellerBase.html"
  return temp

def create_group(request):
  if request.method=="POST":
    group_name=request.POST.get("group_name")
    group_name=''.join(e for e in group_name if e.isalnum())
    print(group_name)
    group_name=group_name.replace(" ","-")
    if create_group:
      try:
        ustore,created=Store.objects.get_or_create(store_owner=request.user)
        grp=Group.objects.create(group_name=group_name,store=ustore)
        GroupUsers.objects.get_or_create(user=request.user,group=grp,is_admin=True)
        messages.success(request,"Your Group is Created")
        return redirect("chat")
      except Exception as ex:
        print(ex)
        messages.error(request,"Please Enter Unique group name")
        return redirect("chat")
        
    
def video_chat(request):
  return render(request,"video.html")