import os
import sys
import django
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
load_dotenv()  # Load environment variables

# Path to your project
path = "/home/TSE2025/Geneva"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Geneva.settings")

application = get_wsgi_application()
