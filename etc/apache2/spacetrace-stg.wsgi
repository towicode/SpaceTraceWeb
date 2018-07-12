"""
WSGI config for testdjangoprj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import sys
import signal
import logging
import traceback
import time

from django.core.wsgi import get_wsgi_application

from raven.contrib.django.middleware.wsgi import Sentry

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
os.environ['CELERY_LOADER'] = 'django'
os.environ['SENTRY_DSN'] = 'https://4da4e85b42be488f844f1bab5c5ec153:c589f087c3754309a39b251a93b874fb@sentry.io/55531'
logger = logging.getLogger('wsgi')

# Warning, Sentry WSGI middleware wrapper seems to hide exceptions from syslog.
# Need to create/find/or add our own middleware to capture that too.

try:
    application = Sentry(get_wsgi_application())
except Exception as e:
    if('mod_wsgi' in sys.modules):
        logger.error(traceback.format_exc())
        logger.error(e)
        traceback.print_exc()
        sys.stdout.write(str(e))
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
