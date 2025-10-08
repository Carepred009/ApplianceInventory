from django import forms
from django.core.validators import RegexValidator


from .models import Customer, Category, Supplier, Product, Order, Checkout, ProductName

#For sending Email from the System
class EmailForm(forms.Form):
   sender_name = forms.CharField(label="Your Name",max_length=255 )
   recipient_email =  forms.EmailField(label="Recipient Email")
   message = forms.CharField(widget=forms.Textarea, label="Type your message")


#Testing for crispy-bootstrap5
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name','last_name','email','number','address')
        widgets = {
            'first_name': forms.TextInput(attrs={ 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={ 'placeholder': 'Email'}),
            'number': forms.TextInput(attrs={'placeholder': 'Enter 11 digits mobile number'}),
            'address': forms.Textarea(attrs={ 'placeholder': 'Address'}),
        }

        '''
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'number':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter 11 digits mobile number'}),
            'address': forms.Textarea(attrs={'class':'form-control','placeholder':'Address'}),
        }
        '''

#Testing crispy-bootstrap5
# Edit and update in add_category_branch
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','description')

        widgets = {
                'category_name':forms.TextInput(attrs={'placeholder':'Category Name'}),
                'description':forms.TextInput(attrs={'placeholder':'Description'})
        }
        '''
        Remove it before deployment
          widgets = {
                'category_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Category Name'}),
                'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
        }
        '''


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('supplier_name','number','email','address')

        widgets  = {
            'supplier_name': forms.TextInput(attrs={'placeholder':'Supplier Name'}),
           'number':forms.TextInput(attrs={'placeholder':'Phone Number'}),
            'email':forms.EmailInput(attrs={'placeholder':'Suppliers Email'}),
            'address':forms.Textarea(attrs={'placeholder':'Supplier Address'})
        }

        '''
         widgets  = {
            'supplier_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Supplier Name'}),
           'number':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Suppliers Email'}),
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'Supplier Address'})
        }
        '''

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','product_description','quantity','price','category','supplier','product_image']

        widgets = {
            'product_name':forms.Select(attrs={'placeholder':'Product Name'}),
            'product_description':forms.TextInput(attrs={'placeholder':'Product Description'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 10000}),             # ✅ Correct
            'category':forms.Select(attrs={'placeholder':'Select Category'}),
            'supplier': forms.Select(attrs={'placeholder':'Select Supplier'}),
            'transaction_date':forms.DateTimeInput(attrs={'type':'datetime-local'}),

        }

        '''
             widgets = {
            'product_name':forms.Select(attrs={'class':'form-control','placeholder':'Product Name'}),
            'product_description':forms.TextInput(attrs={'class':'form-control','placeholder':'Product Description'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}),             # ✅ Correct
            'category':forms.Select(attrs={'class':'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'transaction_date':forms.DateTimeInput(attrs={'type':'datetime-local'}),

        }
        '''


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer','product','order_quantity','amount']
        widgets ={
            'customer':forms.Select(),
            'product':forms.Select(attrs={'id': 'product-select'}),
            #'order_date':forms.DateTimeInput(attrs={'type':'datetime-local'}), dili na ipas display sa template

            'order_quantity':forms.NumberInput(attrs={'minx':1,'max':'10000','id': 'quantity-input'}),# 'id': 'quantity-input'
            'amount': forms.NumberInput(attrs={'readonly': 'readonly','id': 'amount-field'}), #'readonly': 'readonly','id': 'amount-field'

        }

        '''
             widgets ={
            'customer':forms.Select(attrs={'class':'form-control'}),
            'product':forms.Select(attrs={'class':'form-control','id': 'product-select'}),
            #'order_date':forms.DateTimeInput(attrs={'type':'datetime-local'}), dili na ipas display sa template

            'order_quantity':forms.NumberInput(attrs={'class':'form-control','minx':1,'max':'10000','id': 'quantity-input'}),# 'id': 'quantity-input'
            'amount': forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly','id': 'amount-field'}), #'readonly': 'readonly','id': 'amount-field'

        }
        
        
        '''




class ProductNameForm(forms.ModelForm):
    class Meta:
        model = ProductName
        fields = ['product_name']

        widgets = {
            "product_name":forms.TextInput(attrs={'placeholder':'Product Name'})
        }

        '''
        widgets = {
            "product_name":forms.TextInput(attrs={'class':'form-control','placeholder':'Product Name'})

        }
        '''



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
