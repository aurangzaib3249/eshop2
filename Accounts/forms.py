from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm
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
        fields=["full_name",'email','phone','address',"country","avatar","password"]
        widgets={
            "full_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Full Name"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email Address"}),
            "phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Phone Number"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Complete Address"}),
            "country":forms.Select(attrs={"class":"form-control"}),
            "avatar":forms.FileInput(),
            "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter password"}),
        }
    def save(self, *args, **kwargs):
        self.instance.set_password(self.cleaned_data['password'])
        self.instance.user_type="Seller"
        return super().save(*args, **kwargs)
class BuyerRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','address',"country","avatar","password"]
        widgets={
            "full_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Full Name"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email Address"}),
            "phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Phone Number"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Complete Address"}),
            "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter password"}),
            "country":forms.Select(attrs={"class":"form-control"}),
            "avatar":forms.FileInput(),
        }
    def save(self, *args, **kwargs):
        self.instance.set_password(self.cleaned_data['password'])
        return super().save(*args, **kwargs)
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
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
))