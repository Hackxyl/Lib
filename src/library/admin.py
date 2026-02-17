from django.contrib import admin
from .models import Book, Borrow


# Custom admin for Borrow to show 'returned' and other fields

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date', 'returned', 'approved')
    list_filter = ('returned', 'approved', 'borrow_date')
    search_fields = ('user__username', 'book__title')


admin.site.register(Book)
