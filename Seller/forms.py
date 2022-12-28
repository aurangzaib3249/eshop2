
from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    def __init__(self ,*args, **kwargs):
        user=kwargs.pop('user', None)
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['product_category'].queryset=Category.objects.filter(store__store_owner=user)
    class Meta:
        model=Product
        fields=["store","product_name","product_category","product_desc","purchase_price","sale_price","discounted_price","purchase_quantity","remaining_quantity"]
        widgets={
          "product_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Product Name"}),
          "product_category":forms.Select(attrs={"class":"form-control","placeholder":"Select Category"}),
          "product_desc":forms.TextInput(attrs={"class":"form-control","placeholder":"Description"}),
          "purchase_price":forms.NumberInput(attrs={"class":"form-control","placeholder":"purchase price"}),
          "sale_price":forms.NumberInput(attrs={"class":"form-control","placeholder":"sale price"}),
          "discounted_price":forms.NumberInput(attrs={"class":"form-control","placeholder":"discounted price"}),
          "purchase_quantity":forms.NumberInput(attrs={"class":"form-control","placeholder":"Purchase Quantity"}),
          "remaining_quantity":forms.NumberInput(attrs={"class":"form-control","placeholder":"Remaining Quantity"}),
          "store":forms.HiddenInput(),
         
          
        }

class StoreForm(forms.ModelForm):
  class Meta:
    model=Store
    fields=["store_owner","store_name","store_country","store_address","store_phone","opening_time","closing_time"]
    widgets={
      "store_owner":forms.HiddenInput(),
      "store_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Store Name"}),
      "store_country":forms.Select(attrs={"class":"form-control","placeholder":"Store Location"}),
      "store_address":forms.TextInput(attrs={"class":"form-control","placeholder":"Complete Address"}),
      "store_phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Store Phone Number"}),
      "opening_time":forms.TimeInput(attrs={"class":"form-control vTimeField",'type': 'time'}),
      "closing_time":forms.TimeInput(attrs={"class":"form-control vTimeField",'type': 'time'}),
    }
    
class ReviewForm(forms.ModelForm):
  class Meta:
    model=OrderReview
    fields=["full_name","orderitem","review","rate"]
    widgets={
      "full_name":forms.TextInput(),
      "orderitem":forms.Select(attrs={"class":"form-control","placeholder":"Enter Store Name"}),
      "review":forms.Select(attrs={"class":"form-control","placeholder":"Store Location"}),
      "rate":forms.TextInput(attrs={"class":"form-control","placeholder":"Complete Address"}),
     
    }
    
