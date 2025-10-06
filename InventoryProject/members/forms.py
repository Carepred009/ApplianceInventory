from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from .models import Profile
from django import forms




class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','position','date_hire','department'] #do not add the user foreign key

    #for the current use the view will handle the current use
        widgets = {
                'position': forms.Select(attrs={'class':'form-control','placeholder':'Position'}),
                'date_hire':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                'department':forms.Select(attrs={'class':'form-control','placeholder':'Department'})

        }

#for crispy form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


'''
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

'''