from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TravelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.travel'
    verbose_name = _("Travel")
