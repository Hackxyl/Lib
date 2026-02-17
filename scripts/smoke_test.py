import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ruby.settings')
django.setup()
from django.test import Client

c = Client()
urls = ['/', '/accounts/login/', '/admin/', '/books/', '/home/', '/borrow/']
for u in urls:
    try:
        r = c.get(u)
        print(u, r.status_code)
        if r.status_code >= 500:
            print('ERROR PAGE:', r.content[:300])
    except Exception as e:
        print(u, 'EXCEPTION', type(e).__name__, e)
