from django import template

from django.template.defaultfilters import stringfilter
from Accounts.models import User
from django.utils.safestring import mark_safe
register = template.Library()

register = template.Library()
from Seller.models import ProductWishList


@register.filter(name="cart_count")
def cart_count(cart):
 
  return len(cart)

@register.filter(name="to_lower")
def to_lower(value):
 
  return value.lower()

@register.filter(name="get_product_qty")
def get_product_qty(cart,id):
  id=str(id)
  if id in cart:
    return cart[id]
  else:
    return 0
  
@register.filter(name="get_order_item_price")
def get_order_item_price(cart,item):
  price=item.get_price()
  id=item.id
  qty=cart[str(id)]
  price=price*qty
  
  return price
  
@register.simple_tag
def check_in_userWishlist(uid,pid):
      res=ProductWishList.objects.filter(user__id=uid,product__id=pid).first()
      if res:
        return False
      else:
        return True
      
      
@register.filter(name='mention', is_safe=True)
@stringfilter
def mention(value):
  import re

  text = "@RayFranco is answering to @jjconti, this is a real '@username83' but this is an@email.com, and this is a @probablyfaketwitterusername";

  result = re.findall("(^|[^@\w])@(\w{1,15})", value)
  html='<p class="text-secondary">'
  for i in result:
   
    html=html+f'<a href="#">@{i[1]}</a>'
    value=value.replace("@"+i[1],"")
  html=html+value+"</p>"
  return mark_safe(html)
  
@register.filter(name='get_template', is_safe=True)
def get_template(type):
  temp="BuyerBase"
  if type=="Seller":
    temp="SellerBase"
  return temp
  
  
@register.filter(name='remove_slash', is_safe=True)
def remove_slash(url):
  
  return url.replace("/","")
  
  
@register.filter(name='get_unread_chat', is_safe=True)
def get_unread_chat(chats,user1):
  
  flag=False
  for i in chats:
    print(i.sender)
    if i.sender==user1:
      flag=True
      break
  print(flag)
  return flag
