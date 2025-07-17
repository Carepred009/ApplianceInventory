from itertools import product
from msilib.schema import ListView

from django.forms import DecimalField
from django.shortcuts import render

from django.contrib import messages
from django.urls import reverse_lazy, reverse

from .models import Customer, Category, Supplier, Product, Stocks, Order
from .forms import CustomerForm, CategoryForm, SupplierForm, ProductForm, OrderForm

from django.views.generic import TemplateView, CreateView, ListView, DetailView

from django.db.models import Sum, F, Q


# Create your views here.

class OrderDisplay(ListView):
    model = Order
    template_name = 'order_display.html'
    context_object_name = 'orders'



class OrderAccept(CreateView):
    model = Order
    template_name = 'order.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        customer_id = self.request.GET.get('customer_id')
        if customer_id:
            initial['customer'] = customer_id  # Use customer ID here
        return initial

    def get_context_data(self, **kwargs): # para sa pag kwenta pila total amount and bayad by  amount = quantity* price
        context = super().get_context_data(**kwargs)# # para sa pag kwenta pila total amount and bayad by  amount = quantity* price
        context['product_prices'] = {p.product_id: float(p.price) for p in Product.objects.all()} # para sa pag kwenta pila total amount and bayad by  amount = quantity* price
        return context


    def form_valid(self, form):
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['order_quantity']
        form.instance.amount = product.price * quantity
        return super().form_valid(form)

class SearchResultView(ListView):
    model = Stocks
    template_name = 'search.html'
    context_object_name = 'results'
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Stocks.objects.filter(
                Q(product__product_name__icontains=query) #| Q(product__product_name__icontains=query)
            )
        else:
            return Stocks.objects.none() # Or `.all()` if you want to show everything by default


'''
    def get_queryset(self):
        return Stocks.objects.filter(

            Q(product__product_name__icontains="Refrigator") | Q(product__product_name__icontains="Washing")
        )
'''
    #def get_queryset(self):
       # return  Stocks.objects.filter(product__product_name__icontains="Refrigator")
    #queryset =  Stocks.objects.filter(product__product_name__icontains="Refrigator") #the product__ the Foreign key relation between Stocks and Product models #prodduct_name__ is from the Product model



class StocksView(ListView):
    model = Stocks
    template_name = 'stocks.html'
    context_object_name = 'stocks'



class ProductView(CreateView):
    model = Product
    template_name = 'product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        quantity = form.cleaned_data.get('quantity')
        price = form.cleaned_data.get('price')
        total = quantity * price
        form.instance.sum_per_transaction = total  # You called it sum_per_transaction in model

        # Terminal print
        print(f"[DEBUG] Creating product: {form.cleaned_data.get('product_name')}")
        print(f"[DEBUG] Quantity: {quantity}, Price: {price}")
        print(f"[DEBUG] Total (sum_per_transaction): {total}")

        # User message
        messages.success(self.request, 'Successfully added Product')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error On Saving!')
        return super().form_invalid(form)

class SupplierView(CreateView):
    model = Supplier
    template_name = 'supplier.html'
    form_class = SupplierForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request,'Added Supplier Successfully')
        return  super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Error on Adding! Check inputs!')
        return super().form_invalide(form)



class CategoryView(CreateView):
    model = Category
    template_name = 'category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request,'Added Category Successfully')
        return  super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Error on Adding! Check inputs!')
        return super().form_invalide(form)

class CustomerView(CreateView):
    model = Customer
    template_name = 'customer.html'
    form_class = CustomerForm
    success_url = reverse_lazy('order')

    def get_success_url(self):
        return reverse('order-create') + f'?customer_id={self.object.pk}'

    def form_valid(self, form):
        messages.success(self.request,'Customer Added Successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Error Occur in Saving Customer')
        return super().form_invalid(form)


class BaseView(TemplateView):
    template_name = "base.html"

