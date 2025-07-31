#vendors/apps.py
#Vendor-specific functionality, shop profiles, and verification

from django.apps import AppConfig


class VendorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendors'
