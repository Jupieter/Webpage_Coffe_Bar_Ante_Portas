from django.apps import AppConfig
import os
from django.conf import settings

class C_appConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'c_app'
    path = os.path.join(settings.BASE_DIR, 'c_app')
