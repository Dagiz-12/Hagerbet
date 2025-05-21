from django.conf import settings
from django.template.loader import get_template
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hagerbet.settings')
django.setup()


print("Template directories:", settings.TEMPLATES[0]['DIRS'])

try:
    t = get_template('allauth/layouts/entrance.html')
    print(f"SUCCESS! Template found at: {t.origin}")
except Exception as e:
    print(f"ERROR: {str(e)}")
    print("\nDEBUG: Trying to find template manually...")
    from django.template.loaders.filesystem import Loader
    loader = Loader()
    try:
        source, origin = loader.get_template('allauth/layouts/entrance.html')
        print(f"MANUAL SUCCESS! Found at: {origin}")
    except Exception as e2:
        print(f"MANUAL ERROR: {str(e2)}")
