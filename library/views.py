from django.shortcuts import render, redirect, get_object_or_404
from users.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book, Borrow, contactMessage, Category
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

User = get_user_model()


# Create your views here.


@login_required
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
    books = Book.objects.select_related('category').order_by('category')
    return render(request, 'home/books.html', {'books': books})


# Example for contact view
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Persist the contact message to the database
        try:
            contactMessage.objects.create(name=name, email=email, message=message)
        except Exception:
            # If saving fails, continue and report via email attempt
            pass
        try:
            send_mail(
                subject=f"New contact message from {name}",
                message=message,
                from_email=email,
                recipient_list=['hackxyl58@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Thank you for contacting us!")
        except Exception as e:
            messages.error(request, f"Email failed: {e}")
        return redirect('contact')
    return render(request, 'home/contact.html')


def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form},
    )


def book_search(request):
    query = request.GET.get('q')
    books = []

    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)

    return render(request, 'home/search_results.html', {
        'books': books,
        'query': query
    })


def book_list(request):
    category_id = request.GET.get('category')
    books = Book.objects.select_related('category').all()
    if category_id:
        books = books.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'home/book_list.html', {'books': books, 'categories': categories})


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if the book is already borrowed and not yet returned (pending or approved)
    already_borrowed = Borrow.objects.filter(book=book, returned=False).exists()
    if already_borrowed:
        messages.error(request, "This book is already borrowed and cannot be borrowed again until it is returned.")
        return redirect('books')

    if request.method == "POST":
        Borrow.objects.create(
            user=request.user,
            book=book,
            borrow_date=timezone.now(),
            approved=False,
            returned=False
        )
        messages.info(request, "Your borrow request has been submitted and is pending approval.")
        return redirect('borrowed_books')

    # Make sure this template exists!
    return render(
        request,
        'home/borrow_book.html',
        {'book': book},
    )


class LogoutView(View):
    def post(self, request):
        # Add any pre-logout logic here
        logout(request)
        # Add any post-logout logic here
        return redirect('login')  # Or your logout success page

    # For GET requests (not recommended but sometimes used)
    def get(self, request):
        logout(request)
        return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


# Settings view
@login_required
def settings_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Your settings have been updated.')
        return redirect('settings')
    return render(request, 'accounts/settings.html', {'user': request.user})


def is_admin_or_librarian(user):
    return user.is_authenticated and user.role in ['admin', 'librarian']


@user_passes_test(is_admin_or_librarian)
def admin_dashboard(request):
    context = {
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
        'total_borrows': Borrow.objects.count(),
        'overdue_returns': Borrow.objects.filter(book__available=False).count(),  # Optional logic
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def borrowed_books_view(request):
    user = request.user
    if user.is_staff or getattr(user, 'role', None) in ['admin', 'librarian']:
        # Admins/librarians see all borrowed books, ordered by category for grouping
        borrowed_books = (
            Borrow.objects.select_related(
                'book__category',
                'user',
            )
            .order_by('book__category')
        )
    else:
        # Students see only their own borrowed books, ordered by category
        borrowed_books = (
            Borrow.objects.select_related(
                'book__category',
                'user',
            )
            .filter(user=user)
            .order_by('book__category')
        )
    return render(request, 'home/borrowed_books.html', {'borrowed_books': borrowed_books})


@staff_member_required
def approve_borrowed_books(request):
    pending_borrows = Borrow.objects.filter(approved=False)
    if request.method == "POST":
        borrow_id = request.POST.get("borrow_id")
        borrow = get_object_or_404(Borrow, id=borrow_id)
        borrow.approved = True
        borrow.book.available = False  # Mark book as unavailable
        borrow.book.save()
        borrow.save()

        messages.success(request, "Borrow request approved and user notified by email.")
        return redirect('approve_borrowed_books')
    return render(
        request,
        'admin/approve_borrowed_books.html',
        {'pending_borrows': pending_borrows},
    )


@login_required
def return_book(request, borrow_id):
    # Staff can return any book, users can only return their own
    if request.user.is_staff:
        borrow = get_object_or_404(Borrow, id=borrow_id)
    else:
        borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
    if not borrow.return_date:
        borrow.return_date = timezone.now()
        borrow.returned = True
        borrow.book.available = True
        borrow.book.save()
        borrow.save()
        messages.success(request, "Book returned successfully and is now available for borrowing!")
    else:
        messages.info(request, "This book has already been returned.")
    return redirect('borrowed_books')


def test_email(request):
    send_mail(
        subject='Test Email',
        message='This is a test email sent using certifi!',
        from_email='your_email@gmail.com',
        recipient_list=['your_email@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent.")


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Only allow borrowing if available
        if book.available:
            Borrow.objects.create(
                user=request.user,
                book=book,
                borrow_date=timezone.now(),
                approved=False,  # or True if you want instant approval
                returned=False
            )
            book.available = False  # Optionally mark as unavailable immediately
            book.save()
            messages.success(request, "Your borrow request has been submitted and is pending approval.")
        else:
            messages.error(request, "Sorry, this book is not available.")
        return redirect('borrowed_books')
    return render(request, 'home/book_detail.html', {'book': book})
