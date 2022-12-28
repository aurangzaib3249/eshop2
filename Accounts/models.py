
import imp
from random import randint, random
from time import timezone
from django.db import models
import uuid
from django.contrib.auth.models import UserManager,AbstractBaseUser,AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from .managers import *
import datetime as dt

from django.utils import timezone as tz
user_type=(
    ("Seller","Seller"),
    ("Buyer","Buyer"),
)
def get_unique():

    return str(dt.datetime.now())+str(uuid.uuid4().hex[:10].upper())+str(randint(0,10000))
def profile_path(instance, filename):
    return "Profiles/{0}/{1}".format(instance.email, filename)

user_status=(
    ("Online","Online"),
    ("Offline","Offline"),
)
class User(AbstractUser):
    username=None
    full_name=models.CharField(_("Full Name"),null=True,blank=True,max_length=35)
    email=models.EmailField(_("E-mail"),unique=True)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=150)
    country=CountryField(blank_label='(Select Country)')
    user_type=models.CharField(choices=user_type,default="Buyer",max_length=20)
    avatar=models.ImageField(upload_to=profile_path,null=True,blank=True)
    chat_name=models.CharField(max_length=100,null=True,blank=True,unique=True)
    notification_id=models.UUIDField(default=uuid.uuid4(),editable=False)
    status=models.CharField(choices=user_status,max_length=20,default="Offline")
    
    last_seen=models.DateTimeField(default=tz.now)
    USERNAME_FIELD="email"
    objects=CustomUserManager()
    REQUIRED_FIELDS=[]
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    
    @property
    
    def get_full_name(self):
        return self.full_name
    def has_perm(self,perm,obj=None):
        if self.user_type=="Seller" or self.is_superuser:
            return True
        else:
            return False
    def has_module_perm(self,app_label):
        if self.user_type=="Seller" or self.is_superuser:
            return True
        else:
            return False
    @property
    def get_country(self):
        if self.country:
            if self.country=="(Select Country)":
                return "Country not Selected"
            else:
                return self.country
        return "Country not Selected"
   
    def is_first_time(self):
        if self.last_login:
            return False
        else:
            return True
    def get_group(self):
        from Buyer.models import Group
        
        grp=Group.objects.filter(store__store_owner=self).first()
        
        return grp
            
    def save(self,*args, **kwargs):
        
        
        if self.user_type=="Seller":
            from Seller.models import Store
            store,created=Store.objects.get_or_create(store_owner=self)
            if created:
                print("store is created")
        super().save(*args, **kwargs)
        if not self.chat_name:
            if self.full_name:
                self.chat_name=self.full_name.replace(" ","_")
                self.chat_name=self.chat_name+str(self.pk)
            else:
                self.chat_name=self.email.split("@")[0]
        
            self.chat_name=self.chat_name+str(self.pk)
            self.save()
        
            