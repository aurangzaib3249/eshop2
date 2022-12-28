import imp
from django.urls import path

from .views import *
urlpatterns = [
    path("",HomeView.as_view(),name="buyer_home"),
    path("profile",Profile.as_view(),name="buyer_profile"),
    path("store",StoreView.as_view(),name="store"),
    path("products",ProductView.as_view(),name="buyer_products"),
    path("addCart/<pk>",AddCart.as_view(),name="addCart"),
    path("addCart",AddCartView.as_view(),name="addCart"),
    path("remove_item_single_from_cart/<pk>",RemoveItemFromCartSingle.as_view(),name="remove_single_item"),
    path("RemoveItemFromCart/<pk>",RemoveItemFromCart.as_view(),name="remove_item"),
    path("cart",CartView.as_view(),name="buyer_cart"),
    path("payment_received",Received.as_view(),name="payment_received"),
    path("payment_cencel",CancelPayment.as_view(),name="payment_cencel"),
    path("product_detail/<str:pk>/",ProductDetails.as_view(),name="product_detail"),
    path("product_add_wishlist",AddProductTOWishList.as_view(),name="product_add_wishlist"),
    path("wishlist",MyWishList.as_view(),name="wishlist"),
    path("wishlist_item_remove/<str:pk>",RemoveItemFromWishList.as_view(),name="wishlist_item_remove"),
    path("wishlist_item_remove_ajax",RemoveItemFromWishListAjax.as_view(),name="wishlist_item_remove_ajax"),
    path("myaccount",MyAccount.as_view(),name="account_buyer"),
    path("product_review",ReviewOrderItem.as_view(),name="product_review"),
    path("store_details/<str:pk>",Stores_details.as_view(),name="store_details"),
    
    
    
]

