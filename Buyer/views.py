from itertools import product
from multiprocessing.resource_sharer import stop
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import View,ListView,DeleteView,DetailView,FormView,CreateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Seller.models import *
from Accounts.forms import *
from .models import *
from django.contrib import messages
from django.contrib.messages import constants as tags
from django.db.models import *
from django.http import HttpResponse,JsonResponse
from .forms import *
from Seller.serializers import  *
from Seller.forms import StoreForm
import stripe
from django.conf import settings
from django.utils.translation import gettext_lazy as _

stripe.api_key = settings.STRIPE_SECRET_KEY
MESSAGE_TAGS = {
    tags.INFO: 'info',
    tags.SUCCESS: 'success',
    tags.ERROR: 'error',
}
class HomeView(LoginRequiredMixin,ListView):
    template_name="buyer_home.html"
    context_object_name="recent_products"
    def get_queryset(self):
        print("DFfrrfreg")
        return Product.objects.all().order_by("-id")[:10]
    def get_context_data(self, **kwargs):
        data=super().get_context_data(**kwargs)
        data["all_product"]=Product.objects.all()
        data["discounted_product"]=Product.objects.filter(discounted_price__isnull=False)
        return data
    
class Profile(View):
    form_class=ProfileForm
    def get(self,request,**kwargs):
        profile=ProfileForm(instance=request.user)
        return render(request,"profile.html",{"profile":profile})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated")
        else:
            return render(request,"profile.html",{"profile":form})
        return redirect("buyer_profile")
class StoreCreateView(CreateView):
    form_class=StoreForm
    template_name="store.html"
    def get_form(self):
        form=super().get_form(self.form_class)
        form.base_fields['store_owner'] = forms.CharField(initial=self.request.user,disabled=True)
        return form
    def get_initial(self):
        initial=super().get_initial()
        initial["store_owner"]=self.request.user
    def form_valid(self,form):
        form.instance.store_owner = self.request.user
        user=User.objects.get(id=self.request.user.id)
        user.user_type="Seller"
        user.save()
        messages.success("Your store is created")
        return super().form_valid(form)
    
        
class StoreView(View):
    form_class=StoreForm
    def get(self,request,**kwargs):
        store=Store.objects.filter(store_owner=request.user).first()
        if store:
            form=StoreForm(instance=store)
        else:
            initial = {'store_owner': request.user}
            form=StoreForm(initial=initial)
        return render(request,"store.html",{"form":form})
    def post(self, request, *args, **kwargs):
        store=Store.objects.filter(store_owner=request.user).first()
        if store:
            form = self.form_class(request.POST or None,instance=store)
            if form.is_valid():
                form.save()
                messages.success(request,"Store Details Updated")
                return redirect("home")
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                user=User.objects.get(id=request.user.id)
                user.user_type="Seller"
                user.save()
                messages.success(request,"Your Store has beed created")
                return redirect("home")
        if form.errors:
            return render(request,"store.html",{"form":form})
        return redirect("store")
class ProductDetails(View):
    def get(self,request,pk=None):
        if pk:
            visited=request.session.get("visited")
            if not visited:
                visited=[]
            product=Product.objects.filter(id=pk).first()
            comments=ProductComments.objects.filter(product=product).order_by("-comment_at")
            reviews=OrderReview.objects.filter(orderitem__product=product)
            users=comments.values_list("user__full_name",flat=True)
            
            recent_products=None
            if visited:
                    recent_products=Product.objects.filter(id__in=visited)
            if product:
                if pk not in visited:
                    visited.append(pk)
                request.session["visited"]=visited
                return render(request,"product_details.html",{"product":product,"recent_products":recent_products,"reviews":reviews,"comments":comments,"users":users})
        messages.info(request,"Product not found")
        return redirect("buyer_products")
    def post(self,request,pk=None):
        comment=request.POST.get("comment")
        pk=request.POST.get("productid")
        print(comment,pk)
        product=Product.objects.filter(id=pk).first()
        if product:
            comment=ProductComments.objects.create(user=request.user,product=product,comment=comment)
            messages.success(request,"comment submited")
        else:
            messages.error(request,"Error")
        return redirect("product_detail",pk=pk)
class ProductView(View):
    template_name="products.html"
    context_object_name="products"
    def get(self,request):
        product=Product.objects.all().order_by("-id")[:20]
        categories=Category.objects.all().distinct()
        
        dict={"products":product,"categories":categories}
        return render(request,"products.html",dict)
    def post(self,request):
        search=request.POST.get("search")
        product=Product.objects.filter(Q(product_name__icontains=search)| Q(product_category__category__icontains=search) | Q(product_desc__icontains=search))
        count=product.count()
        categories=Category.objects.all().distinct()
        
       
        dict={"products":product,"count":count,"categories":categories}
        return render(request,"products.html",dict)
class Stores_details(View):
    def get(self,request,pk=None):
        if pk:
            store=Store.objects.filter(id=pk).first()
            if store:
                products=Product.objects.filter(store=store)
                dict={"store":store,"products":products}
                dict={"store":store,"products":products}
            else:
                messages.error(request,"Store Not found")
                dict={"store":{},"products":[]}
            
        else:
            messages.error(request,"Store Not found")
            dict={"store":{},"products":[]}
        return render(request,"stores.html",dict)
class AddCart(View):
    def get(self,request,pk=None):
        if pk:
            try:
                product_list=request.session.get("product_list")
                if product_list:
                    if pk not in product_list:
                        product_list[pk]=1
                    else:
                        product_list[pk]=product_list[pk]+1
                else:
                    product_list={}
                    product_list[pk]=1
                request.session["product_list"]=product_list
                messages.success(request,"Product added in your cart,Count in your cart is "+str(len(product_list)))
            except Product.DoesNotExist:
                messages.error(request,"Product not found")
        else:
            messages.error(request,"Product not found")
        url=request.META.get('HTTP_REFERER') #redirect to previous url
        return redirect(url)
class AddCartView(View):
    def get(self,request):
        pk=request.GET.get("id")
        if pk:
            try:
                product_list=request.session.get("product_list")
                if product_list:
                    if pk not in product_list:
                        product_list[pk]=1
                    else:
                        product_list[pk]=product_list[pk]+1
                else:
                    product_list={}
                    product_list[pk]=1
                request.session["product_list"]=product_list
                return JsonResponse({"msg":f'Product added in your cart,item in your cart is {(len(product_list))} and this product qty is {product_list[pk]}',"status":200})
                
            except Product.DoesNotExist:
                return JsonResponse({"msg":"Product not found "+str(len(product_list)),"status":404})
                
        else:
            return JsonResponse({"msg":"Product not found "+str(len(product_list)),"status":404})
        
class RemoveItemFromCartSingle(View):
    def get(self,request,pk=None):
        if pk:
            product_list=request.session.get("product_list")
            if product_list:
                if pk in product_list:
                    if product_list[pk]==1:
                        product_list.pop(pk)
                        messages.success(request,"Product removed from your cart")
                    else:
                        product_list[pk]=product_list[pk]-1
                        messages.success(request,"Product quantity decreased by 1")
                    
                else:
                    messages.error(request,"Product Not exist in your cart")
            else:
                product_list={}
            request.session["product_list"]=product_list
        else:
            messages.error(request,"Product Not exist in your cart")
        url=request.META.get('HTTP_REFERER') #redirect to previous url
        return redirect(url)
class RemoveItemFromCart(View):
    def get(self,request,pk=None):
        if pk:
            product_list=request.session.get("product_list")
            if product_list:
                if pk in product_list:
                    product_list.pop(pk)
                    messages.success(request,"Product removed from your cart")
                else:
                    messages.error(request,"Product Not exist in your cart")
            else:
                product_list={}
            request.session["product_list"]=product_list
        else:
            messages.error(request,"Product Not exist in your cart")
        url=request.META.get('HTTP_REFERER') #redirect to previous url
        return redirect(url)
        
class CartView(View):
    def get(self,request):
        django_product_list=[]
        product_list=request.session.get("product_list")
        if not product_list:
            product_list={}
            request.session["product_list"]=product_list
        keys=product_list.keys()
        django_product_list=Product.objects.filter(id__in=keys)
        total = sum(v.get_price()*product_list[str(v.id)] for v in django_product_list)
        dict={"products":django_product_list,"sum":total,'key':settings.STRIPE_PUBLISHABLE_KEY}
        return render(request,"cart.html",dict)
    def post(self,request, *args, **kwargs):
        product_list=request.session.get("product_list")
        orders=[]
        if product_list:
            address=ShippingAddres.objects.filter(user=request.user).first()
            if address:
                keys=product_list.keys()
                django_product_list=Product.objects.filter(id__in=keys)
                for product in django_product_list:
                    order,created=Order.objects.get_or_create(user=request.user,store=product.store,address=address,status="Pending")
                    if created:
                        orders.append(order)
                    qty=product_list[str(product.id)]
                    product_price=product.get_price()
                    orderitem=OrderItem.objects.create(product=product,price=product_price,qty=qty)
                    order.orderItems.add(orderitem)
                    order.save()
                token = self.request.POST.get('stripeToken')
                
                amount=0
                for order in orders:
                    amount=amount+order.get_order_amount
                print(amount)
                amount = int(amount * 100)
                #4242 4242 4242 4242 use any code date and zip
                try:
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="USD",
                        source=token
                    )
                    for order in orders:
                    
                        order.status="Awaiting Shipment"
                        order.save()
                    messages.success(self.request, "Your Order has been confirmed ")
                    request.session["product_list"]={}
                    return redirect("payment_received")
                except Exception as ex:
                    for order in orders:
                        order.status="Awaiting Payment"
                        order.save()
                    messages.error(self.request, ex)
            else:
                messages.error(self.request, _("Address is required"))
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            request.session["product_list"]={}
            messages.error(self.request, _("Cart is empty"))
            return redirect("buyer_products")
        request.session["product_list"]={}
        return redirect("payment_cencel")
class Received(TemplateView):
    template_name="success.html"
class CancelPayment(TemplateView):
    template_name="cancel.html"
class MyAccount(View):
    def get(self,request):
        all_Shipped_orders=Order.objects.filter(user=request.user,is_review=True)
        current_orders=Order.objects.filter(user=request.user,is_review=False).order_by("-id")
        return render(request,"my_account.html",{"current_orders":current_orders,"all_Shipped_orders":all_Shipped_orders})

class ReviewOrderItem(View):
    def post(self,request):
        orderid=request.POST.get("orderitemId")
        rating=request.POST.get("rating"+orderid)
        comment=request.POST.get("comment")
        if comment and orderid:
            orderItem=OrderItem.objects.filter(id=orderid).first()
            if orderItem:
                OrderReview.objects.create(orderitem=orderItem,review=comment,rate=rating,full_name=request.user)
                orderItem.is_reviewed=True
                orderItem.save()
                order=Order.objects.filter(orderItems=orderItem).first()
                order.check_orderitems_rating()
            messages.success(request,"Thank you")
        else:
            messages.success(request,"Review Comment is required")
        return redirect(request.META.get('HTTP_REFERER'))
    
class MyWishList(View):
    def get(self,request):
        products=ProductWishList.objects.filter(user=request.user)
        return render(request,"product_wish_list.html",{"products":products})
    
class RemoveItemFromWishList(View):
    def get(self,request,pk):
        if pk:
            product=ProductWishList.objects.get(id=pk)
            if product:
                product.delete()
                messages.success(request,"Product removed from wish list")
            else:
                messages.success(request,"Product not found")
            return redirect("wishlist")
        
class RemoveItemFromWishListAjax(View):
    def get(self,request):
        pk=request.GET.get("id")
        print(pk)
        if pk:
            
            
            product=ProductWishList.objects.filter(product__id=pk,user=request.user).first()
            print(product)
            if product:
                product.delete()
                return JsonResponse({"msg":"Product removed from wish list","status":200})
            else:
                return JsonResponse({"msg":"Product nout found","status":404,"form":None})
        return JsonResponse({"msg":"Product nout found","status":404,"form":None})
        
           
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
    
    
