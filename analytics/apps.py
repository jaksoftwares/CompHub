# analytics/apps.py
# Dashboard metrics, reporting, and business intelligence
from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics'
