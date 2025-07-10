from itertools import product
from msilib.schema import ListView

from django.shortcuts import render

from django.contrib import messages
from django.urls import reverse_lazy

from .models import Customer, Category, Supplier, Product, Stocks, Order
from .forms import CustomerForm, CategoryForm, SupplierForm, ProductForm

from django.views.generic import TemplateView, CreateView, ListView


# Create your views here.



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
        messages.success(self.request, 'Successfully added Product')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error On Saving!')
        return super().form_invalid(form)

'''
    def form_valid(self,form):
        # Save the customer instance
        product = form.save()

        # Now create a Stocks entry using product data
        Stocks.objects.create(
            product = product,
            supplier = product.supplier,
            percentage = '0%'  # or any default value you want
        )
        return super().form_valid(form)


        messages.success(self.request, 'Successfully added Product')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error On Saving!')
        return super().form_invalid(form)
'''
'''
  

'''
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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request,'Customer Added Successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Error Occur in Saving Customer')
        return super().form_invalid(form)


class BaseView(TemplateView):
    template_name = "base.html"

