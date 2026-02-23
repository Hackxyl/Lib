# your_app/custom_email_backend.py

import ssl
import certifi
from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        # Force SSL context to use certifi bundle
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        super().__init__(*args, **kwargs)
