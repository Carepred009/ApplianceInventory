from lib2to3.fixes.fix_input import context

from .forms import SignUpForm, UserProfile

from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import  User
from django.views.generic import TemplateView, CreateView, DetailView

from .models import Profile


# Create your views here.

class SignUpView(CreateView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request,'Register Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Error in Registration')
        return super().form_invalid(form)


class UserDetailView( DetailView):
    model = User
    template_name = "profile/user_profile.html"
    context_object_name = "user_obj"

    def get_object(self):
        # This gives the current logged-in user instance
        return self.request.user


class UserProfileView(CreateView):
    model = Profile
    form_class = UserProfile
    template_name = 'profile/create_profile.html'
    success_url = reverse_lazy('create_profile') #redirect after sucessfull creation


    def form_valid(self, form):
        # attach current user
        form.instance.user = self.request.user #auto-assign logged-in user
        return super().form_valid(form)


    #Display the current User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user #pass the use to the template
        return context


