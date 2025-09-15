from django.views.generic import TemplateView
from django.urls import path

from django.views.generic import TemplateView
from .views import (BaseView, CustomerView, CategoryView, SupplierView, ProductView, StocksView, SearchResultView,
                    OrderAccept, OrderDisplay, SpecifiedProductView, CheckOutView,
                    CheckoutDisplayView, IncomingStocksView, SalesChartView, CustomerListView, SupplierListView,
                    SupplierUpdateView, SupplierDeleteView, CustomerUpdateView, CustomerDeleteView, EmailContactView, ProductNameView, PieChartView
                    )


from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',BaseView.as_view(), name="home"),

    #without using view in the views.py
    path('home_design/',TemplateView.as_view(template_name='base2.html'), name="home_design"),

    path('send_email/', EmailContactView.as_view(), name="send_email"),
    path('success_email/success/', TemplateView.as_view(template_name='send_email_success.html'), name="send_email_success"),

    path('stocks/',StocksView.as_view(), name="stocks"),

    path('create_product_name/', ProductNameView.as_view(), name="create_product_name"),
    path('product/',ProductView.as_view(), name="product"),


    path('supplier/', SupplierView.as_view(), name="supplier"),
    path('supplier_list/', SupplierListView.as_view(), name="supplier_list"),
    path('update_supplier/<int:pk>/',SupplierUpdateView.as_view(), name="update_supplier"),
    path('delete_supplier/<int:pk>/',SupplierDeleteView.as_view(), name="delete_supplier"),

    path('category/', CategoryView.as_view(), name="category"),

    path('customer_list/',CustomerListView.as_view(), name="customer_list"),
    path('customer/', CustomerView.as_view(), name="customer"),
    path('customers_update/<int:pk>/', CustomerUpdateView.as_view(), name="customers_update"),
    path('customer_delete/<int:pk>/',CustomerDeleteView.as_view(), name="customers_delete"),


    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('search_result/',SearchResultView.as_view(), name="search"),

    path('order/', OrderAccept.as_view(), name='order-create'),

    path('order_display/',OrderDisplay.as_view(), name="order_display"),

    path('stocks_per_product/', SpecifiedProductView.as_view() ,name="search_stock"), #sum the quantity per product

    #path('select_product/',SelectProductView.as_view(), name="select_product"),
   # path('update_product/<int:pk>/', UpdateProductView.as_view(), name="update_product"),

    #path('new_arrival/',StockArrivalView.as_view(), name="stock_arrival")

    path('check_out/<int:pk>/',CheckOutView.as_view(), name="checkout"), #This is DetailView

    path('checkout/',CheckoutDisplayView.as_view(), name="checkout_display"), #this is ListView

    path('incoming/',IncomingStocksView.as_view(), name="incoming"),

    path('sales_chart/', SalesChartView.as_view(), name="sales_chart"),
    path('pie_chart/',PieChartView.as_view(), name="pie_chart"),


]