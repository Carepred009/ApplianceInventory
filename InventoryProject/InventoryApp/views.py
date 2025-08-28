from itertools import product
from lib2to3.fixes.fix_input import context

from django.conf import settings
from django.contrib.messages import success
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse


from .models import Customer, Category, Supplier, Product, Stocks, Order, Checkout, IncomingStocks, ProductName
from .forms import CustomerForm, CategoryForm, SupplierForm, ProductForm, OrderForm, EmailForm, ProductNameForm  #StockArrivalForm #ProductUpdateForm,
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, FormView, DeleteView
from django.db.models import Sum, F, Q

# Create your views here.

class EmailContactView(FormView):
    template_name = 'contact_email.html'
    form_class = EmailForm
    success_url = reverse_lazy('send_email_success')

    def form_valid(self, form):
        #this is from the form that we use in form_class
        sender_name = form.cleaned_data['sender_name']
        recipient_email = form.cleaned_data['recipient_email']
        message = form.cleaned_data['message']

        subject = f"New Email from {sender_name}"
        full_message = f"From:{sender_name} <{recipient_email}> \n\n Messsage: \n {message}"

        send_mail(subject, full_message, settings.EMAIL_HOST_USER, [recipient_email])

        return super().form_valid(form)



class SalesChartView(TemplateView):
    template_name = 'sales_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # query the Checkout model
        checkouts = Checkout.objects.all()

        # gets the product_name from ProductName model because it FK and use for loop to get all data
        context['labels'] = [checkout.product_name.product_name for checkout in checkouts]
        context['data']  = [checkout.checkout_quantity for checkout in checkouts]
        return context

class PieChartView(TemplateView):
    template_name = 'PieCharts_stocks.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        #total_quantity = Product.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0

        grouped_data = (
            Product.objects
            .values('product_name__product_name')
            .annotate(total_count = Sum('quantity'))
           # .order_by('-quantity') do not include it because the pie chart will be slice according to when you insert it
        )
        context['labels'] = [item['product_name__product_name'] for item in grouped_data]
        context['counts'] = [item['total_count'] for item in grouped_data]
        return context

class UpdateCustomer(UpdateView):
    model = Customer

class CheckoutDisplayView(ListView):
    model = Checkout
    template_name = 'display_checkout.html'
    context_object_name = 'checkouts'
    paginate_by = 10
    #ordering = []

class CheckOutView(DetailView):
    model = Order
    template_name = 'check_out_details.html'
    context_object_name = 'checkouts'

    def post(self, request, *args, **kwargs):
        order = self.get_object() # we can use the variables in Order model with order.order_id example
        product = order.product # We can access Product model from Model by order.product but we must product.product_id example

        # Get Stock object related to the product
        stock = get_object_or_404(Stocks, product=product)


        # Prevent negative stock
        if product.quantity < order.order_quantity:
            # You can show a message instead of redirect if using messages framework
            messages.error(self.request,"No more stocks")
            return redirect('order_display')

        #Adjust the total amount of the current product count and actual count
        # Deduct product stock
        product.quantity -= order.order_quantity
        product.save()


        #send an email upon checksout the order  send_mail() function is already in django.
        send_mail(
            subject="Order Confirmation",
            message= f"Thank you for your Order, {order.customer.first_name}."
                      f"You bought {order.order_quantity} x {product.product_name}."
                        f"for a total of {order.amount}.",
            from_email= "djangoproject583@gmail.com", #Use the email that for the store only
            recipient_list=[order.customer.email], # get the customer email
            fail_silently= False,
        )


        #Insert into Checkout model after Clicking Chekcout button
        Checkout.objects.create(
            product_name = order.product.product_name, # careful: you have ProductName FK
            customer_name = order.customer,
            product_price = order.product,
            checkout_total = order.amount,
            checkout_quantity =  order.order_quantity

        )
        # order.status = 'confirmed'
        order.save()
        # Delete the order after checkout
        order.delete()
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

        # return to the home if the product quanity is greater than order quantity
        if quantity > product.quantity:
            messages.error(self.request,'More the the actual stocks')
            return self.form_invalid(form)

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

    def get_queryset(self):
        queryset = super().get_queryset()
        product_name = self.request.GET.get("product")

        if product_name:
            queryset = queryset.filter(product__product_name = product_name)
        return queryset

    # this is function is remove working but the context is remove in the template
    #get the total or sum of all products in the Stocks model
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_quantity = Stocks.objects.aggregate(Sum('actual_count')) ['actual_count__sum'] or 0  # ['actual_count__sum'] or 0 add this to prevent display the model attribute
        context['total_quantity'] = total_quantity
        return  context









class IncomingStocksView(ListView):
    model =  IncomingStocks
    template_name = 'incoming_stocks.html'
    context_object_name = 'incoming'


class SpecifiedProductView(ListView):
    model = Product
    template_name = 'specified_product.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Group by product_name and sum quantity for each
        total_per_product = (
            Product.objects
            .values('product_name__product_name')  # assuming ProductName model has a 'name' field
            .annotate(total_quantity=Sum('quantity'))
        )

        context['total_per_product'] = total_per_product
        return context

class ProductNameView(CreateView):
    model =  ProductName
    template_name = 'product_name.html'
    form_class = ProductNameForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request,"Added Product Name Successfully")
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request,"Invalid Input")
        return super().form_invalid(form)

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

#create Supplier
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
        return super().form_invalid(form)

#Display all supplier
class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers_list.html'
    context_object_name = 'suppliers'

#Update the Supplier
class SupplierUpdateView(UpdateView):
    model = Supplier
    template_name = 'update_supplier.html'
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_list')


    def form_valid(self, form):
        messages.success(self.request,"Update Successfully!")
        return  super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Error on updating!')
        return super().form_invalid(form)

#delete the supplier
class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'delete_supplier.html'
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        messages.success(self.request,"Deleted Successfully!")
        return  super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"Error on Delete!")
        return super().form_invalid(form)

#Creates category of the product
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

    #Hold the customer name and id to use in Order model
    def get_success_url(self):
        return reverse('order-create') + f'?customer_id={self.object.pk}'

    def form_valid(self, form):
        messages.success(self.request,'Customer Added Successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Error Occur in Saving Customer')
        return super().form_invalid(form)

#Delete Customer
class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer_delete.html'
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        messages.success(self.request,'Deleted Successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Error On Delete!')
        return super().form_invalid(form)
#Update Customer
class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'customers_update.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        messages.success(self.request,"Update Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Update Error')
        return super().form_invalid(form)
#Display all Customer
class CustomerListView(ListView):
    model = Customer
    template_name = 'customers_list.html'
    context_object_name = 'customers'
    paginate_by = 10

class BaseView(TemplateView):
    template_name = "home.html"

