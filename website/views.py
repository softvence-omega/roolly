from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


# Create your views here.
def home(request):
    # check to see if loggin in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You have been logged in..!! {request.user.username}")
            return redirect('home')
        else:
            messages.error(request, "There was An Error Loggin In, Try Again Please..")
            return redirect('home')
    else:
        return render(request, 'home.html', {})



# login
def login_user(request):
    pass


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
    