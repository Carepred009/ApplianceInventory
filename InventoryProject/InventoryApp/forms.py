from django import forms
from unicodedata import category

from .models import Customer,Category,Supplier, Product


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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','product_description','quantity','price','category','supplier','product_image')

        widgets = {
            'product_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name'}),
            'product_description':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Description'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}),             # ✅ Correct
            'category':forms.Select(attrs={'class':'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'transaction_date':forms.DateTimeInput(attrs={'type':'datetime-local'}),

        }