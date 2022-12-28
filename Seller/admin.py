
from django.contrib import admin
from .models import *
from django import forms

class ProductAdmin(admin.ModelAdmin):
    model=Product
    list_display=("product_name","product_category","get_price","remaining_quantity","is_available")
    list_filter=("is_available","product_category")
    fieldsets=(
        ("Product Details",{"fields":("product_name","product_category","image","remaining_quantity","is_available","purchase_quantity","discounted_price","sale_price","purchase_price","product_desc")}),
        ("Non Change able Fields",{"fields":("create_at","store")})
    )
    add_fieldsets=(
         ("Create Product", {
            'classes': ('wide',),
            'fields': ("store","product_name","product_category","image","remaining_quantity","is_available","purchase_quantity","discounted_price","sale_price","purchase_price","product_desc")}
        ),
    )
    def get_queryset(self, request):
        r=super(ProductAdmin,self).get_queryset(request)
        
        return r.filter(store__store_owner=request.user)
    def get_form(self, request, obj, **kwargs):
        form = super(ProductAdmin,self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        store=Store.objects.filter(store_owner=request.user)
        form.base_fields['store'] = forms.CharField(initial=store,disabled=True,help_text="You cannot edit this field")
        return form
class CategoryAdmin(admin.ModelAdmin):
    list_display=("category","store")
    list_filter=("store",)
    model=Category
    fieldsets=(
        ("Category Details",{"fields":("category","store")}),
        
    )
    add_fieldsets=(
         ("Create Product", {
            'classes': ('wide',),
            'fields': ("store","category")}
        ),
    )
    def get_queryset(self, request):
        r=super(CategoryAdmin,self).get_queryset(request)
        
        return r.filter(store__store_owner=request.user)
    def get_form(self, request, obj, **kwargs):
        form = super(CategoryAdmin,self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        store=Store.objects.filter(store_owner=request.user)
        form.base_fields['store'] = forms.CharField(initial=store,disabled=True,help_text="You cannot edit this field")
        return form
class StoreAdmin(admin.ModelAdmin):
    model=Store
    list_display=("store_owner","store_name","store_phone","block_store","store_country","is_open","avg_rating")
    list_filter=("block_store",)
    fieldsets=(
        ("Store Details",{"fields":("store_owner","store_name","store_phone","store_address","image","opening_time","closing_time","create_at","block_store","store_country")}),
        
    )
    add_fieldsets=(
         ("Create Product", {
            'classes': ('wide',),
            'fields': ("store_owner","store_name","store_phone","store_address","image","opening_time","closing_time","block_store","store_country")}
        ),
    )
    def get_queryset(self, request):
        r=super(StoreAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return r
        return r.filter(store_owner=request.user)
    def get_form(self, request, obj, **kwargs):
        form = super(StoreAdmin,self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
       
        form.base_fields['store_owner'] = forms.CharField(initial=request.user,disabled=True,help_text="You cannot edit this field")
        return form
class OrderAdmin(admin.ModelAdmin):
    model=Order
    list_display=("user",'store',"get_order_amount","coupon","order_date","status")
    list_filter=("status","is_review",'store')
   
    fieldsets=(
        ("Order Details",{"fields":("user",'store',"is_review","orderItems","coupon","order_date","status","address")}),
        
    )
    add_fieldsets=(
         ("Create Order", {
            'classes': ('wide',),
            'fields': ("user",'store',"orderItems","is_review","coupon","order_date","address")}
        ),
    )
    def get_queryset(self, request):
        r=super(OrderAdmin,self).get_queryset(request)
        
        if request.user.is_superuser :
            return r
        return r.filter(store__store_owner=request.user)
    def get_form(self, request, obj, **kwargs):
        form = super(OrderAdmin,self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        form.base_fields['store'] = forms.CharField(initial=request.user,disabled=True,help_text="You cannot edit this field")
        return form
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
class OrderItemAdmin(admin.ModelAdmin):
    model=OrderItem
    list_display=("product","get_orderitem_price","price","qty")
    list_filter=("price",)
   
    fieldsets=(
        ("Order Details",{"fields":("product","price","qty")}),
        
    )
    add_fieldsets=(
         ("Create Order", {
            'classes': ('wide',),
            'fields': ("product","price","qty")}
        ),
    )
    def get_queryset(self, request):
        r=super(OrderItemAdmin,self).get_queryset(request)
        if request.user.is_superuser :
            return r
        return r.filter(order__store__store_owner=request.user)
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
class CouponAdmin(admin.ModelAdmin):
    model=Coupon
    list_display=("store","code","amount","min_amount","is_valid","expire_at","created_at")
    
   
    fieldsets=(
        ("Order Details",{"fields":("store","code","amount","min_amount","expire_at","created_at")}),
        
    )
    add_fieldsets=(
         ("Create Order", {
            'classes': ('wide',),
            'fields': ("store","code","amount","min_amount","expire_at","created_at")}
        ),
    )
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def get_queryset(self, request):
        r=super(CouponAdmin,self).get_queryset(request)
        if request.user.is_superuser :
            return r
        return r.filter(store__store_owner=request.user)
class ShippingAddressAdmin(admin.ModelAdmin):
    model=ShippingAddres
    list_display=("user","address","country","zip_code")
    fieldsets=(
        ("Order Details",{"fields":("user","address","country","zip_code")}),
        
    )
    add_fieldsets=(
         ("Create Order", {
            'classes': ('wide',),
            'fields': ("user","address","country","zip_code")}
        ),
    )
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser   

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderReview)
admin.site.register(ProductWishList)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Store,StoreAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(ShippingAddres,ShippingAddressAdmin)
