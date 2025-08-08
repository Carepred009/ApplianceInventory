from itertools import product
from lib2to3.fixes.fix_input import context
from msilib.schema import ListView
from subprocess import check_output

from django.contrib.messages.apps import update_level_tags
from django.forms import DecimalField
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages
from django.urls import reverse_lazy, reverse

from .models import Customer, Category, Supplier, Product, Stocks, Order, Checkout, IncomingStocks
from .forms import CustomerForm, CategoryForm, SupplierForm, ProductForm, OrderForm  #StockArrivalForm #ProductUpdateForm,

from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, FormView

from django.db.models import Sum, F, Q


# Create your views here.


class SalesChartView(TemplateView):
    template_name = 'sales_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Aggregate total quantity sold per product
        sales_data = (
            Checkout.objects
            .values("product_name")
            .annotate(total_sold = Sum("checkout_quantity"))
            .order_by("product_name")
        )

        # Prepare data for Charts.js
        context["labels"] = [item["product_name"] for item in sales_data]
        context["data"] = [item["total_sold"] for item in sales_data]

        return context


class UpdateCustomer(UpdateView):
    model = Customer

class CheckoutDisplayView(ListView):
    model = Checkout
    template_name = 'display_checkout.html'
    context_object_name = 'checkouts'

    


class CheckOutView(DetailView):
    model = Order
    template_name = 'check_out_details.html'
    context_object_name = 'checkouts'

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        product = order.product

        # Get Stock object related to the product
        stock = get_object_or_404(Stocks, product=product)

        # Prevent negative stock
        if product.quantity < order.order_quantity:
            # You can show a message instead of redirect if using messages framework
            messages.error(self.request,"No more stocks")
            return redirect('order_display')

        #Adjust the total amount of the current product count and actual count

       # product.sum_per_transaction -= order.amount
       # stock.save(update_fields=['total_price'])

        # Deduct product stock
        product.quantity -= order.order_quantity
        product.save()


        #Insert into Checkout model after Clicking Chekcout button
        Checkout.objects.create(
            product_name = order.product.product_name, # careful: you have ProductName FK
            customer_name = order.customer,
            product_price = order.product,
            checkout_total = order.amount,
            checkout_quantity =  order.order_quantity

        )
        # Redirect to sucess page
        #return  redirect('')

        # Sync Stock.actual_count with new product quantity
        #stock.actual_count = product.quantity
        #stock.save(update_fields=['actual_count'])


        # (Optional) Mark as confirmed — you might want to add a "status" field later
        # order.status = 'confirmed'
        order.save()
        return redirect('order_display')


class OrderDisplay(ListView):
    model = Order
    template_name = 'order_display.html'
    #context_object_name = 'orders'  if Using pagination remove this and use the Django Built in page_obj
    paginate_by = 6 # Show 10 products per page



class OrderAccept(CreateView):
    model = Order
    template_name = 'order.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_display')


    def get_initial(self):
        initial = super().get_initial()
        customer_id = self.request.GET.get('customer_id')
        if customer_id:
            initial['customer'] = customer_id  # Use customer ID here
        return initial

    #get the price of the selected product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Get specific product (e.g., latest one)
        specific_product = Product.objects.last()
        context['specific_product'] = specific_product

    def form_valid(self, form):
         # get the current User is use model by the instance user
        form.instance.user = self.request.user  # Only 1 form_valid() shoud be use

           # Calculate the Total amount
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['order_quantity']
        form.instance.amount = product.price * quantity
        return super().form_valid(form)



    def get_context_data(self, **kwargs): # para sa pag kwenta pila total amount and bayad by  amount = quantity* price
        context = super().get_context_data(**kwargs)# # para sa pag kwenta pila total amount and bayad by  amount = quantity* price
        context['product_prices'] = {p.product_id: float(p.price) for p in Product.objects.all()} # para sa pag kwenta pila total amount and bayad by  amount = quantity* price
        return context



class SearchResultView(ListView):
    model = Stocks
    template_name = 'search.html'
    context_object_name = 'results'
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Stocks.objects.filter(                   # Not working if you want to search is converted to foreign key
                Q(product__product_name__product_name__icontains=query) | Q(supplier__supplier_name__icontains=query)  # FieldError at /inventory/search_result/ #Unsupported lookup 'icontains' for ForeignKey or join on the field not permitted.
            )
        else:
            return Stocks.objects.none() # Or `.all()` if you want to show everything by default


class StocksView(ListView):
    model = Stocks
    template_name = 'stocks_movement.html'
    #context_object_name = 'stocks'  #remove this if you want pagination and use the built-in  page_obj
    paginate_by = 5 #show 5 rows of result per page number

class IncomingStocksView(ListView):
    model =  IncomingStocks
    template_name = 'incoming_stocks.html'
    context_object_name = 'incoming'

class SpecifiedProductView(DetailView):
    model = Stocks
    template_name = 'specified_product.html'
    context_object_name = 'products'


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
        #Make sure how the hell is save into the the model an database
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

