from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from towima.forms import SignUpForm

# Define a signup view. This will provide the user with a signup page and the correct functionality.
def signup(request):
    if request.method == 'POST':                # When we POST the form.
        form = SignUpForm(request.POST)
        if form.is_valid():                     # Check if the form is valid.
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')         
    else:                                       # When we GET the form.
        form = SignUpForm()                     # Provide the form to the user.
    return render(request, 'signup.html', {'form': form})