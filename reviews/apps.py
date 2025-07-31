# reviews/apps.py
#Product reviews, ratings, and feedback system

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
