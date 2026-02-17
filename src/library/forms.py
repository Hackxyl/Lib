from django import forms
from .models import Borrow
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Get your custom user model
CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to form fields
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({
                'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500'
            })

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['borrow_date', 'return_date']  # Add any fields you need
        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }
