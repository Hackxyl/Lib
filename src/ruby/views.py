from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from library.models import Book, Borrow
from django.utils import timezone

User = get_user_model()



def test_view(request):
    return HttpResponse("View is working!")





@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def settings_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('settings')
    
    return render(request, 'accounts/settings.html')



def is_admin_or_librarian(user):
    return user.is_authenticated and user.role in ['admin', 'librarian']

@user_passes_test(is_admin_or_librarian)
def admin_dashboard(request):
    context = {
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
        'total_borrows': Borrow.objects.count(),
        'overdue_returns': Borrow.objects.filter(book__available=False, user__is_active=True).count(),  # Adjust as needed
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def borrow_confirm(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        Borrow.objects.create(user=request.user, book=book, borrow_date=timezone.now())
        book.available = False
        book.save()
        return redirect('borrowed_books')

    return render(request, 'library/borrow.html', {'book': book})


