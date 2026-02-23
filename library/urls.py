from django.urls import path
from . import views
from .views import admin_dashboard, approve_borrowed_books
from library.views import borrow_book
from .views import return_book


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('borrowed-books/', views.borrowed_books_view, name='borrowed_books'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('approve-borrows/', approve_borrowed_books, name='approve_borrowed_books'),

    path('return-book/<int:borrow_id>/', return_book, name='return_book'),

]
