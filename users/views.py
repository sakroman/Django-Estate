from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.views.generic import CreateView, View
from django.http import JsonResponse
from users.forms import SignUpForm
from .models import *


class RegisterView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        user = form.save()
        login(self.request, user)
        return valid
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class LoginPageView(View):
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return JsonResponse({'success': True, 'success_url': self.success_url })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid email or password.'})
        else:
            return JsonResponse({'success': False, 'message': 'Empty fields.'})
