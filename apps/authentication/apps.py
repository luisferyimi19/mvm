from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    """docstring for AuthenticationConfig"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"
    verbose_name = _("Authentication and Authorization")
