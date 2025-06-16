from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book
from django.contrib import messages
from .models import Book,contactMessage
from django.core.mail import send_mail as send_email




# Create your views here.
def home(request):
    """
    Render the home page.
    """
    return render(request, 'home/home.html')  # Ensure you have a 'home.html' template in your templates directory

def about(request):
    """
    Render the about page.
    """
    return render(request, 'home/about.html')  # Ensure you have an 'about.html' template in your templates directory
 
def books(request):
    
    return render(request, 'home/books.html')

def contact(request):
    if request.method == "POST":

        # handle form submission here
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # send email to site owner
        send_email(
            subject=f"New contact message from {name}",
            message=message,
            from_email=email,
            recipient_list=['hackxyl58@gmail.com'],
        )
        messages.success(request, "Thank you for contacting us!")
        return redirect('contact')
    # Always return a response for GET or other methods
    return render(request, 'home/contact.html')


def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, log the user in after registration
            
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})  # Ensure you have a 'register.html' template in your templates directory

def book_search(request):
    query = request.GET.get('q')
    books = []

    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)

    return render(request, 'home/search_results.html', {
        'books': books,
        'query': query
    })







