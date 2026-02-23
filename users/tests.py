from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model


class RegistrationTests(TestCase):
    def post_registration(self, username='testuser', password='Password123!', email='test@example.com', role='student'):
        return self.client.post(
            reverse('register'),
            data={'username': username, 'email': email, 'password1': password, 'password2': password, 'role': role},
            follow=True,
        )

    @override_settings(AUTO_LOGIN_AFTER_REGISTRATION=True)
    def test_auto_login_after_registration(self):
        """When AUTO_LOGIN_AFTER_REGISTRATION=True the user should be authenticated after registering."""
        resp = self.post_registration()
        # After following redirects, request user should be authenticated
        user = resp.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        # Ensure the user exists in DB
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_no_auto_login_when_disabled(self):
        resp = self.post_registration(username='noauto')
        user = resp.wsgi_request.user
        # Should not be authenticated automatically
        self.assertFalse(user.is_authenticated)
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='noauto').exists())

