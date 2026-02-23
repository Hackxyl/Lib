from django.core.management.base import BaseCommand
from library.models import Book, Borrow


class Command(BaseCommand):
    help = 'Set book.available=True if all borrows are returned, else False.'

    def handle(self, *args, **kwargs):
        fixed = 0
        for book in Book.objects.all():
            if Borrow.objects.filter(book=book, returned=False).exists():
                if book.available:
                    book.available = False
                    book.save()
                    fixed += 1
            else:
                if not book.available:
                    book.available = True
                    book.save()
                    fixed += 1
        self.stdout.write(self.style.SUCCESS(f'Fixed availability for {fixed} books.'))
