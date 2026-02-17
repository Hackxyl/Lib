
# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.conf import settings
from .forms import CustomUserCreationForm

def register(request):
    """
    Handles user registration with custom form
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # Optional: Automatically log in the user after registration if enabled
            if getattr(settings, 'AUTO_LOGIN_AFTER_REGISTRATION', False):
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, "Registration successful and you're now logged in.")
                    return redirect('home')
                # If authentication fails, fall back to the non-logged-in flow below

            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})