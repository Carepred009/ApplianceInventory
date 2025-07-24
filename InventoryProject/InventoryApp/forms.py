from django import forms
from unicodedata import category

from .models import Customer, Category, Supplier, Product, Order


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name','last_name','email','number','address')

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'number':forms.TextInput(attrs={'class':'form-control','placeholder':'Your number'}),
            'address': forms.Textarea(attrs={'class':'form-control','placeholder':'Address'}),

        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','description')

        widgets = {
                'category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Category Name'}),
                'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('supplier_name','number','email','address')

        widgets  = {
            'supplier_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Supplier Name'}),
            'number':forms.TextInput(attrs={'class':'form-control','placeholder':'Suppliers Number'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Suppliers Email'}),
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'Supplier Address'})
        }
'''
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','product_description','quantity','price','category','supplier','product_image']  # only include fields you want updated

        widgets = {
            'product_name':forms.TextInput(attrs={'class':'form-control','readonly': 'readonly'}), # 'readonly': 'readonly' prevent from editing while updating some fields
            'product_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Description'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}),  # ✅ Correct
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'transaction_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
'''
'''
class StockArrivalForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(min_value=1)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())
    price = forms.DecimalField(max_digits=10,decimal_places=2, widget=forms.NumberInput(attrs={'steps':'0.01'})) # Optional: for decimal step
'''


'''
#this form is for new Arrival of Products
class StockArrivalForm(forms.Form):
    product =  forms.ModelChoiceField(queryset=Product.objects.all()) # remember that this  from the Foreign key
    quantity = forms.IntegerField(min_value=1, label='Quantity Arrive')
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all()) # remember that this  from the Foreign key
    price = forms.DecimalField(max_digits=10,decimal_places=2, widget=forms.NumberInput(attrs={'steps':'0.01'})) # Optional: for decimal step
'''


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','product_description','quantity','price','category','supplier','product_image')

        widgets = {
            'product_name':forms.Select(attrs={'class':'form-control','placeholder':'Product Name'}),
            'product_description':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Description'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}),             # ✅ Correct
            'category':forms.Select(attrs={'class':'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'transaction_date':forms.DateTimeInput(attrs={'type':'datetime-local'}),

        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer','product','order_quantity','amount','user']

        widgets ={
            'customer':forms.Select(attrs={'class':'form-control'}),
            'product':forms.Select(attrs={'class':'form-control','id': 'product-select'}),
            #'order_date':forms.DateTimeInput(attrs={'type':'datetime-local'}), dili na ipas display sa template
            'order_quantity':forms.NumberInput(attrs={'class':'form-control','minx':1,'max':'10000','id': 'quantity-input'}),# 'id': 'quantity-input'
            'amount': forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly','id': 'amount-field'}), #'readonly': 'readonly','id': 'amount-field'

        }