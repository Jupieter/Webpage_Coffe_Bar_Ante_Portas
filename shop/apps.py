from django.apps import AppConfig
import os
from django.conf import settings


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    path = os.path.join(settings.BASE_DIR, 'shop')