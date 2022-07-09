from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import UserRegistrationForm, UserLoginForm

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            User.objects.create_user(username, email, password)
            return redirect('accounts:user_login')
        return render(request, self.template_name, {'form':form})




class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request):
    	form = self.form_class(request.POST)
    	if form.is_valid():
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')
            return render(request, self.template_name, {'form':form})
