"""
WSGI config for leetqode project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leetqode.settings')

application = get_wsgi_application()
