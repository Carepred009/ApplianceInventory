from tkinter.font import names

from django.urls import path

from .views import (BaseView, CustomerView, CategoryView, SupplierView, ProductView, StocksView, SearchResultView,
                    OrderAccept, OrderDisplay, SpecifiedProductView, CheckOutView,
                    CheckoutDisplayView, IncomingStocksView, SalesChartView, CustomerListView, SupplierListView,
                    SupplierUpdateView, SupplierDeleteView, StocksChartView, CustomerUpdateView, CustomerDeleteView
                    )  # SelectProductView, UpdateProductView   StockArrivalView #StockArrivalView


from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',BaseView.as_view(), name="home"),

    path('stocks/',StocksView.as_view(), name="stocks"),

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

    path('search_stocks/<int:pk>', SpecifiedProductView.as_view() ,name="search_stock"),

    #path('select_product/',SelectProductView.as_view(), name="select_product"),
   # path('update_product/<int:pk>/', UpdateProductView.as_view(), name="update_product"),

    #path('new_arrival/',StockArrivalView.as_view(), name="stock_arrival")

    path('check_out/<int:pk>/',CheckOutView.as_view(), name="checkout"), #This is DetailView

    path('checkout/',CheckoutDisplayView.as_view(), name="checkout_display"), #this is ListView

    path('incoming/',IncomingStocksView.as_view(), name="incoming"),


    path('sales_chart/', SalesChartView.as_view(), name="sales_chart"),
    path('stocks-chart/', StocksChartView.as_view(), name='stocks-chart'),



]