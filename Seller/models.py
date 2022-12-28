from datetime import date
from email.policy import default
from itertools import product
from weakref import proxy
from django.db import models
from Accounts.models import *
from django_countries.fields import CountryField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q,Avg
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from datetime import datetime, time
def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: 
        return check_time >= begin_time or check_time <= end_time
def get_store_path(instance, filename):
    return "Stores/{0}_Store/store_images/{1}".format(instance.store_owner.email, filename)
def get_product_path(instance, filename):
    return "Stores/{0}_Store/product_images/{1}".format(instance.store.store_owner.email, filename)
class Store(models.Model):
    store_owner=models.OneToOneField(User,on_delete=models.CASCADE)
    store_name=models.CharField(max_length=50,unique=True,null=True,blank=True)
    store_country=CountryField(blank_label='(Select Country)')
    store_address=models.CharField(max_length=200,null=True,blank=True)
    store_phone=models.CharField(max_length=30,null=True)
    image=models.ImageField(upload_to=get_store_path)
    opening_time=models.TimeField(null=True,blank=True)
    closing_time=models.TimeField(null=True,blank=True)
    create_at=models.DateTimeField(default=timezone.now)
    block_store=models.BooleanField(default=False)
    def __str__(self):
        return "{0}".format(self.store_owner)
    def delete(self,*args, **kwargs):
        if self.block_store==False:
            raise ValidationError("This Store is already Blocked")
        else:
            self.block_store=False
            return super().save(*args, **kwargs)
    @property
    def is_open(self):
        if self.opening_time and self.closing_time:
            if is_time_between(self.opening_time,self.closing_time):
                return "Open"
            else:
                return "Close"
        else:
            return "Store Time not provided"
    @property
    def avg_rating(self):
        rating=OrderReview.objects.filter(orderitem__product__store=self).aggregate(Avg('rate'))['rate__avg']
        if rating:
            return rating
        else:
            return 5.0
    
    def get_rating_stars(self):
        rate=self.avg_rating
        if not rate:
            rate=5
        else:
            rate=int(rate)
        html=""
        for i in range(0,5):
            if i<rate:
                html=html+"""<span class="fa fa-star checked"></span>"""
            else:
                html=html+"""<span class="fa fa-star"></span>"""
        return mark_safe(html)
class Category(models.Model):
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    category=models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.category
    def save(self,*args, **kwargs):
        if self.pk !=None and self.store.block_store:
            raise ValidationError({"store":"Your Store is blocked by admin,contact with admin"})
        else:
            return super().save(*args, **kwargs)
    def delete(self,*args, **kwargs):
        count=Product.objects.filter(category__category=self.category).count()
        if count>0:
            raise ValidationError("This Category is using in Products")
        else:
            super().delete(*args, **kwargs)
class Product(models.Model):
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=60)
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_desc=models.CharField(max_length=150,null=True,blank=True)
    purchase_price=models.DecimalField(_("Product Purchase Price"),max_digits=6, decimal_places=2)
    sale_price=models.DecimalField(_("Product Sale Price"),max_digits=6, decimal_places=2)
    discounted_price=models.DecimalField(_("Product Discounted price(Optional)"),null=True,blank=True,max_digits=5, decimal_places=2)
    purchase_quantity=models.IntegerField(_("Product Purchase Quantity"))
    remaining_quantity=models.IntegerField(_("Product Remaining Quantity"),null=True,blank=True)
    image=models.ImageField(upload_to=get_product_path,default="product.png")
    create_at=models.DateTimeField(_("date joined"), default=timezone.now)
    updated_at=models.DateTimeField(_("Updated at"), auto_now=True)
    is_available=models.BooleanField(default=True)
    views=models.BooleanField(default=0)
    
    def __str__(self) -> str:
        return "Category of {0} is {1}".format(self.product_name,str(self.product_category))
    def orders_of_product(self):
        return OrderItem.objects.filter(product=self).count()
    def get_product_remaining_percentage(self):
        
        percentage=int(self.remaining_quantity/self.purchase_quantity)
        
        return percentage
    def save(self,*args, **kwargs):
        if self.store.block_store:
            raise ValidationError({"store":"Your Store is blocked by admin,contact with admin"})
        else:
            return super().save(*args, **kwargs)
    def get_product_status(self):
        if self.is_available:
            return "Available"
        else:
            return "Not Available"
    def get_stock_status(self):
        print(self.remaining_quantity)
        if self.remaining_quantity>0:
            return True
        else:
            return False
    def delete(self,*args, **kwargs):
        count=OrderItem.objects.filter(product__id=self.id).count()
        if count>0:
            raise ValidationError("You are not able to delete this Product because this Product is currently using on orders")
        else:
            super().delete(*args, **kwargs)
    def get_price(self):
        if self.discounted_price:
            return self.discounted_price
        else:
            return self.sale_price
    def store_rating(self):
        rating=self.store.avg_rating
        return rating
    def get_rating_stars(self):
        rate=OrderReview.objects.filter(orderitem__product=self).aggregate(Avg('rate'))['rate__avg']
        if not rate:
            rate=5
        else:
            rate=int(rate)
        html=""
        for i in range(0,5):
            if i<rate:
                html=html+"""<span class="fa fa-star checked"></span>"""
            else:
                html=html+"""<span class="fa fa-star"></span>"""
        return mark_safe(html)
    
class Coupon(models.Model):
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    code=models.CharField(max_length=10,null=True,blank=True)
    amount=models.DecimalField(_("Amount"),max_digits=6, decimal_places=2)
    min_amount=models.DecimalField(_("Minimum Amount"),max_digits=6, decimal_places=2)
    expire_at=models.DateTimeField()
    created_at=models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.code
    def save(self,*args, **kwargs):
        if self.pk==None:
            if self.amount<=0:
                raise ValidationError({"amount":"Enter valid discount"})
            if self.min_amount<=0:
                raise ValidationError({"min_amount":"Enter valid minimum amount"})
            return super().save(*args, **kwargs)
        else:
            raise ValidationError("Coupon is not change able")
    def delete(self,*args, **kwargs):
        count=Order.objects.filter(coupon__id=self.id).count()
        if count>0:
            raise ValidationError("You are not able to delete Coupon because this Coupon is currently using on orders")
        else:
            super().delete(*args, **kwargs)
    @property
    def is_valid(self):
        if timezone.now()>self.expire_at:
            return "Yes"
        else:
            return "No"
class ShippingAddres(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=150)
    country=CountryField(blank_label='(Select Country)')
    zip_code=models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.address
    def save(self, *args, **kwargs):
        if self.pk:
            orders=Order.objects.filter(Q(status="Pending") | Q(status="Disputed"),address=self)
            if orders.count()>0:
                raise ValidationError("You are not able to change Address because this address is using on orders")
            else:
                super().save(*args, **kwargs)
        super().save(*args, **kwargs)
    def delete(self,*args, **kwargs):
        count=Order.objects.filter(address__id=self.id).count()
        if count>0:
            raise ValidationError("You are not able to delete Address because this address is using on orders,create new adddress and use in new orders")
        else:
            super().delete(*args, **kwargs)
order_status=(
    #seller controls
    ("Pending","Pending"),
    ("Awaiting Payment","Awaiting Payment"),
    ("Awaiting Shipment","Awaiting Shipment"),
    ("Awaiting Pickup","Awaiting Pickup"),
    ("Pickuped","Pickuped"),
    #seller controls end
    ("Shipped","Shipped"),
    ("Order Confirmed","Order Confirmed"),
    ("Cancelled","Cancelled"),
    ("Declined","Declined"),
    ("Refunded","Refunded"),
    ("Disputed","Disputed"),
    
)
order_statusList=["Pending","Awaiting Payment","Awaiting Shipment","Awaiting Pickup","Pickuped","Shipped","Order Confirmed","Cancelled","Refunded","Disputed"]

order_status2=(   
    #seller controls
    (1,"Pending"),
    (2,"Awaiting Payment"),
    (3,"Awaiting Shipment"),
    (4,"Awaiting Pickup"),
    (5,"Pickuped"),
    #seller controls end
    (6,"Shipped"),
    (7,"Order Confirmed"),
    (8,"Cancelled"),
    (9,"Declined"),
    (10,"Refunded"),
    (11,"Disputed"),
    
)
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    qty=models.IntegerField(default=1)
    is_reviewed=models.BooleanField(default=False)
    def __str__(self) -> str:
        return "Product:{0}".format(str(self.product))
    @property
    def get_orderitem_price(self):
        total_price=float(format(self.price*self.qty,".2f"))
        return total_price
    def is_valid_for_review(self):
        return not self.is_reviewed
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    store=models.ForeignKey(Store,on_delete=models.CASCADE,related_name="StoreOwner",null=True,blank=True)
    orderItems=models.ManyToManyField(OrderItem,blank=True)
    coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True,blank=True)
    order_date=models.DateTimeField(default=timezone.now)
    status=models.CharField(choices=order_status,default="Pending",max_length=50)
    address=models.ForeignKey(ShippingAddres,on_delete=models.CASCADE,null=True,blank=True)
    is_review=models.BooleanField(default=False)
    class Meta:
        pass
    def __str__(self) -> str:
        return "User:{0}-status:{1}".format(self.user,self.status)
    def get_status_key(self):
        for v in order_status2:
            if v[1]==self.status:
               return v[0] 
        return 1
    def check_orderitems_rating(self):
        if not self.is_review:
            items=self.orderItems.all()
            for item in items:
                if item.is_reviewed:
                    continue
                else:
                    return False
            self.is_review=True
            self.status="Order Confirmed"
            self.save()
        return True
    def get_statues(self):
        key=self.get_status_key()
       
        if key<=2:
            return ["Cancelled","Declined","Awaiting Shipment"]
        elif key+1<=5:
            return [order_statusList[key+1]]
        else:
            
            return None
    @property
    def get_coupon(self):
        if self.coupon:
            return self.coupon
        else:
            return "Coupon Not Used"
    def delete(self,*args, **kwargs):
        count=OrderItem.objects.filter(order__id=self.id).count()
        if count>0:
            raise ValidationError("You are not able to delete this order because this order have order items")
        else:
            super().delete(*args, **kwargs)
    @property
    
    def get_order_amount(self):
        items=self.orderItems.all()
        total_price=0
        for item in items:
            total_price=total_price+item.get_orderitem_price
        
        return total_price
    def is_valid_for_review(self):
        if self.status in ["Shipped","Order Confirmed"] and not self.is_review:
            return True
        else:
            return False
        
    def get_order_deleivery_status(self):
        key=self.get_status_key()
        html=""
        if key not in [8,9,10]:
            for i in range(1,7):
                status=order_statusList[i]
                if key>i:
                    html=html+'<div class="step active"> <span class="icon"> <i class="fa fa-check"></i> </span> <span class="text">{}</span> </div>'.format(status)
                else:
                    html=html+'<div class="step "> <span class="icon"> <i class="fa fa-times"></i> </span> <span class="text">{0}</span> </div>'.format(status)
        else:
            html=html+'<div class="step active "> <span class="icon"> <i class="fa fa-check"></i> </span> <span class="text">{0}</span> </div>'.format(self.status)
        return mark_safe(html)
    def delivery_progress(self):
        key=self.get_status_key()
        progress=(key/7)*100
        return int(progress)

    
class OrderReview(models.Model):
    full_name=models.CharField(max_length=50)
    orderitem=models.ForeignKey(OrderItem,on_delete=models.CASCADE,null=True,blank=True)
    review=models.CharField(max_length=200,null=True,blank=True)
    rate=models.IntegerField(default=1,validators=[MinValueValidator(0), MaxValueValidator(5)])
    date=models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.orderitem} {self.rate} {self.date}"
    
    def get_stars(self):
        html=""
        for i in range(1,6):
            if i<=self.rate:
                html=html+'<span class="fa fa-star checked"></span>'
            else:
                html=html+'<span class="fa fa-star"></span> '
        return mark_safe(html)
            
class ProductWishList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'product',)
    def __str__(self) -> str:
        return f"{self.user} like {self.product}"
    
    def get_stock_status(self):
      
        if self.product.remaining_quantity>0:
            return True
        else:
            return False