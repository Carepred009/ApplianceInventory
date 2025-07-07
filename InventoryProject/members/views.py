from django.shortcuts import render

from .forms import SignUpForm

from django.urls import reverse_lazy
from django.contrib import messages

from django.views.generic import TemplateView, CreateView
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
