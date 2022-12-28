from django.urls import path

from .views import *
urlpatterns = [
    path("create/seller",CreateSellerView.as_view(),name="create_seller"),
    path("create/buyer",CreateBuyerView.as_view(),name="create_buyer"),
    path("signup/",SignUpView.as_view(),name="signup"),
    path("login/",UserLoginView.as_view(),name="login"),
    path("logout/",UserLogout,name="logout"),
   
]
