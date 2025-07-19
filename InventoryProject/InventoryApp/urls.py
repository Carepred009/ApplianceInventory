from tkinter.font import names

from django.urls import path

from .views import BaseView, CustomerView, CategoryView, SupplierView, ProductView ,StocksView,SearchResultView,OrderAccept,OrderDisplay, SelectProductView,UpdateProductView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',BaseView.as_view(), name="home"),

    path('stocks/',StocksView.as_view(), name="stocks"),

    path('product/',ProductView.as_view(), name="product"),
    path('supplier/', SupplierView.as_view(), name="supplier"),
    path('category/', CategoryView.as_view(), name="category"),
    path('customer/', CustomerView.as_view(), name="customer"),

    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('search_result/',SearchResultView.as_view(), name="search"),

    path('order/', OrderAccept.as_view(), name='order-create'),
    path('order_display/',OrderDisplay.as_view(), name="order_display"),

    path('select_product/',SelectProductView.as_view(), name="select_product"),
    path('update_product/<int:pk>/', UpdateProductView.as_view(), name="update_product")
]