"""
URL configuration for ruby project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from library.views import home, about, books, contact, book_search
from users.views import register 
from . import views
from library import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from library.views import settings_view, approve_borrowed_books,  return_book


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Assuming you have a home view defined
    path('about/', about, name='about'),  # Assuming you have an about view defined
    path('books/', books, name='books'),  # Assuming you have a books view defined
    path('contact/', contact, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),  # For login, logout, password management, etc.
    path('register/', register, name='register'),  # Assuming you have a register view defined
    path('books/search/', views.book_search, name='book_search'),
    path('library/', include('library.urls')),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('borrowed-books/', views.borrowed_books_view, name='borrowed_books'),
    path('', include('library.urls')),
    path('approve-borrows/', approve_borrowed_books, name='approve_borrowed_books'),
    
    path('return-book/<int:borrow_id>/', return_book, name='return_book'),
    

    # Keep this for other authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)