
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import importlib.util

# Detect Pillow availability and provide a fallback for ImageField
PIL_AVAILABLE = importlib.util.find_spec('PIL') is not None


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)  # Add this line

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,      # Allow NULL in database
        blank=True
    )
    if PIL_AVAILABLE:
        cover = models.ImageField(
            upload_to='book_covers/',
            blank=True,
            null=True,
        )
    else:
        cover = models.CharField(
            max_length=255,
            blank=True,
            null=True,
            help_text='Pillow not installed; store image path as a string',
        )

    def __str__(self):
        return self.title


class contactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    if PIL_AVAILABLE:
        photo = models.ImageField(
            upload_to='profile_photos/',
            blank=True,
            null=True,
        )
    else:
        photo = models.CharField(
            max_length=255,
            blank=True,
            null=True,
            help_text='Pillow not installed; store image path as a string',
        )


# Create your models here.
