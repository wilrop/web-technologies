from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from towima.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')         
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
def home(request):
    template = "home.html"
    context={}
    return render(request, template, context)

def login(request):
    template = "login.html"
    context = {}
    return render(request, template, context)