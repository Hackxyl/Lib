from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import your custom user model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Specify your custom user model
        fields = ("username", "email", "role")  # Add any additional fields you need

