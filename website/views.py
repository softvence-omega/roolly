from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import SignUpForm


# Create your views here.
def home(request):
    return render(request, 'home.html', {})



class LoginUser(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')

# logout
def logout_user(request):
    logout(request)
    messages.info(request, "You Have Been Logout..!!")
    return redirect('home')
    
    
# register
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"You Have Been Register, Welcome.. {request.user.username}")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', { 'form':form })
    
    return render(request, 'register.html', { 'form':form })
    