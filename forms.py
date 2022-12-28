

from django import forms
from .models import *

from django import forms

from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm

        
class CustomChangeForm(UserChangeForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','address',"country","avatar"]
        help_texts = {
            'password ': _(''),
        }

        exclude = ('password',)

class SellerRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','address',"country","avatar","user_type"]
        widgets={
            "full_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Full Name"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email Address"}),
            "phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Phone Number"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Complete Address"}),
            "country":forms.Select(attrs={"class":"form-control"}),
            "avatar":forms.FileInput(),
            "user_type":forms.HiddenInput(attrs={"value":"Seller"}),
        }
class BuyerRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','address',"country","avatar","user_type"]
        widgets={
            "full_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Full Name"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email Address"}),
            "phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Phone Number"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Complete Address"}),
            "country":forms.Select(attrs={"class":"form-control"}),
            "avatar":forms.FileInput(),
            "user_type":forms.HiddenInput(attrs={"value":"Buyer"}),
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["full_name",'phone','address',"country","avatar"]
        widgets={
            "full_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Full Name"}),
           
            "phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Phone Number"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Complete Address"}),
            "country":forms.Select(attrs={"class":"form-control"}),
            "avatar":forms.FileInput(),
            
        }