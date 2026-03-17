import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woody.settings')  # ← ИЗМЕНЕНО: 'woody'

application = get_asgi_application()