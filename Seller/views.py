

from itertools import product
from math import prod
from unicodedata import category
from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator

from django.template.loader import render_to_string

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.messages import constants as tags
# Create your views here.
from .models import *
from .forms import *
MESSAGE_TAGS = {
    tags.INFO: 'info',
    tags.SUCCESS: 'success',
    tags.ERROR: 'error',
    
}

class HomeView(LoginRequiredMixin,ListView):
    template_name="home.html"
    context_object_name="new_orders"
    def get_queryset(self):
        store=Store.objects.filter(store_owner=self.request.user).first()
        
        orders=Order.objects.filter(Q(status="Shipped") | Q(status="Order Confirmed"),store=store)
        return orders
    def get_context_data(self,**kwargs):
        store=Store.objects.filter(store_owner=self.request.user).first()
        
        data = super().get_context_data(**kwargs)
        data["count_orders"]=data["object_list"].count()
        data["new_confirmed_orders"]=Order.objects.filter(Q(status="Pending") | Q(status="Awaiting Shipment")| Q(status="Awaiting Payment"),store=store).order_by("-order_date")
        data["new_confirmed_orders_count"]= data["new_confirmed_orders"].count()
        data["Cancelled_orders"]=Order.objects.filter(Q(status="Cancelled") | Q(status="Declined"),store=store).count()
        
        data["store"]=store
        return data
class OrderList(ListView):
    template_name="orders.html"
    context_object_name="orders"
    def get_queryset(self):
        
        return Order.objects.filter(store__store_owner=self.request.user)
    paginate_by=10
class AddCategory(View):
    def post(self, request, *args, **kwargs):
        
        data=request.POST.get("category")
        store=Store.objects.filter(store_owner=request.user).first()
        cat,created=Category.objects.get_or_create(category=data,store=store)
        print(cat,created,data,request.path)
        messages.success(request, 'Category is added')

        return redirect("seller_home")
    
class CategoryList(ListView):
    template_name="category.html"
    context_object_name="categories"
    def get_queryset(self):
        return Category.objects.filter(store__store_owner=self.request.user)
class Products(View):
    form_class = ProductForm
    def get(self,request,**kwargs):
        products=Product.objects.filter(store__store_owner=request.user).order_by("-id")
        
        categories=Category.objects.filter(store__store_owner=request.user)
        
        initial = {'store': Store.objects.filter(store_owner=request.user).first()}
        form=ProductForm(initial=initial,user=request.user)
        size=int((len(products))*0.3)
        if size==0:
            size=2
        try:
            paginator = Paginator(products, size) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            dict={"products":page_obj,"form":form}
        except Exception as ex:
            print(ex)
            dict={"products":[],"form":form}
        #return render(request, 'list.html', {'page_obj': page_obj})
        return render(request,"manage_products.html",dict)
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST,user=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Product added")
        else:
            print(form.errors)
        print("print")
        return redirect("seller_products")
    @csrf_exempt

    def delete(self,request,**kwargs):
        put = QueryDict(request.body)
        pk = put.get('id')
        try:
            store=Store.objects.filter(store_owner=request.user).first()
            product=Product.objects.get(id=pk,store=store)
            product.delete()
            
            return JsonResponse({"msg":"Product deleted"})
        except Exception as ex:
            try:
                return JsonResponse({"msg":list(ex)[0]})
            except:
               
                return JsonResponse({"msg":"Error during delete product"})
            
class ManageProduct(View):
    def get(self,request):
        pk=request.GET.get("id")
        if pk:
            try:
                product=Product.objects.get(id=pk)
                form=ProductForm(instance=product,user=request.user)
                html=render_to_string("product_edit_form.html",{"form":form,"productId":pk})
                return JsonResponse({"msg":"Data found","status":200,"form":html})
            except Product.DoesNotExist:
                return JsonResponse({"msg":"Product nout found","status":404,"form":None})
        return JsonResponse({"msg":"Product nout found","status":404,"form":None})
                
    def post(self, request, *args, **kwargs):
        id=request.POST.get("productId")
        print(id)
        product=Product.objects.filter(id=id).first()
        if product:
            form = ProductForm(request.POST or None,instance=product,user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request,"Product Updated")
            else:
                print(form.errors)
                messages.success(request,"Error During product updation")
        else:
            messages.success(request,"Error During product updation")
        return redirect("seller_products")
            
class ManageOrderSeller(View):
    def get(self,request):
        id=request.GET.get("id")
        order=Order.objects.filter(id=id).first()
        if order:
            valid_status=order.get_statues
            print(valid_status)
            html=render_to_string("manage_order.html",{"status":valid_status,"order_id":id,"cur":order.status})
            
            return JsonResponse({"msg":"Order found","status":200,"data":html})
        else:
            return JsonResponse({"msg":"Order not found","status":404,"data":None})
    def post(self,request):
        order_status=request.POST.get("order_status")
        order_id=request.POST.get("order_id")
        if  order_id and  order_status and order_status!="---------":
            order=Order.objects.filter(id=order_id).first()
            if order:
                order.status=order_status
                order.save()
                
                messages.success(request,"Order is "+order_status)
            else:
                messages.success(request,"Order is not found")
        else:
                messages.success(request,"error during order updation")
        return redirect(request.META.get('HTTP_REFERER'))
    
    
class MyWishList(View):
    def get(self,request):
        products=ProductWishList.objects.filter(user=request.user)
        return render(request,"wishlist.html",{"products":product})
    
class AddProductTOWishList(View):
    def get(self,request):
        pk=request.GET.get("id")
        if pk:
            try:
                product=Product.objects.get(id=pk)
                addproduct,created=ProductWishList.objects.get_or_create(user=request.user,product=product)
                if created:
                    return JsonResponse({"msg":"Product added in Wish list","status":200})
                else:
                    return JsonResponse({"msg":"Product already exist in wish list","status":200})
            except Product.DoesNotExist:
                return JsonResponse({"msg":"Product nout found","status":404,"form":None})
        return JsonResponse({"msg":"Product nout found","status":404,"form":None})
    
