from django.urls import path

from .views import *
urlpatterns = [
        path("",HomeView.as_view(),name="seller_home"),
        path("orders",OrderList.as_view(),name="seller_orders"),
        path("add_category",AddCategory.as_view(),name="add_category"),
        path("categories",CategoryList.as_view(),name="seller_categories"),
        path("manage_products",Products.as_view(),name="seller_products"),
        path("manage_product",ManageProduct.as_view(),name="manage_product"),
        path("manage_order_seller",ManageOrderSeller.as_view(),name="manage_order_seller"),

]
