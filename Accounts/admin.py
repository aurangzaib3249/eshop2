from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .forms import CustomChangeForm
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form=CustomChangeForm
    readonly_fields=()
    model=User
    list_display=("email",'chat_name','notification_id',"full_name","phone","is_active","last_login")
    list_filter=("last_login","is_active","user_type",)
    
    fieldsets=(
       ("User Information",{"fields":("full_name","phone","address","country","avatar")}),
       ("Non Change able Information ",{"fields":("chat_name","email","user_type","is_active","is_staff","is_superuser","date_joined","last_login")}),
    )
    
    
    add_fieldsets = (
        ("Create Account", {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',"user_type")}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    createonly_fields = ["email"]
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(CustomUserAdmin, self).get_readonly_fields(request, obj))
        createonly_fields = list(getattr(self, 'createonly_fields', []))
        if obj:  
            readonly_fields.extend(createonly_fields)
        return readonly_fields
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser   
    
admin.site.register(User,CustomUserAdmin)