

from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView,FormView
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import *
class CreateSellerView(View):
    form_class=SellerRegistrationForm
    success_url="store"
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect ("home")
        else:
            print(form.errors)
            return redirect("signup")
class CreateBuyerView(View):
    form_class=BuyerRegistrationForm
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)
            return redirect("signup")
class SignUpView(View):
    def get(self,request):
        seller_form=SellerRegistrationForm()
        buyer_form=BuyerRegistrationForm()
        dict={"seller":seller_form,"buyer":buyer_form}
        return render(request,"register.html",dict)
class UserLoginView(auth_views.LoginView):
    form_class=UserLoginForm
    template_name="login.html"
    success_url="home"
def UserLogout(request):
    logout(request)
    return redirect ("login")
    
    
