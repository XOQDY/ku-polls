"""Run Apps."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Run Polls app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
