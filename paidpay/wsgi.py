import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paidpay.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

#application = get_wsgi_application()
application = Cling(get_wsgi_application())
