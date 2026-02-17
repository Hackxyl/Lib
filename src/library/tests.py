from django.test import TestCase
from django.urls import reverse
from .models import contactMessage
from django.core import mail
import importlib
import importlib.util


class ContactTests(TestCase):
    def test_contact_persists_message(self):
        data = {'name': 'Alice', 'email': 'alice@example.com', 'message': 'Hi there'}
        resp = self.client.post(reverse('contact'), data=data, follow=True)
        # contactMessage saved
        self.assertTrue(contactMessage.objects.filter(email='alice@example.com', name='Alice').exists())


class ImageFieldFallbackTests(TestCase):
    def test_cover_field_is_charfield_when_pillow_missing(self):
        # Temporarily force importlib.util.find_spec to report PIL missing, then reload models
        original_find = importlib.util.find_spec

        def fake_find(name):
            if name == 'PIL':
                return None
            return original_find(name)

        importlib.util.find_spec = fake_find
        try:
            mod = importlib.reload(importlib.import_module('library.models'))
            field = mod.Book._meta.get_field('cover')
            from django.db.models import CharField

            self.assertIsInstance(field, CharField)
        finally:
            # restore and reload original module to avoid side effects
            importlib.util.find_spec = original_find
            importlib.reload(importlib.import_module('library.models'))

