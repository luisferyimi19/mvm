from django.contrib.admin import ModelAdmin, register, TabularInline
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.fields import DynamicArrayField
from django_better_admin_arrayfield.forms.widgets import DynamicArrayTextareaWidget
from django.utils.translation import gettext_lazy as _
from apps.travel.models import (
    Portal,
    SocialMediaAccount,
    Travel,
    TravelImage,
    TravelDestination,
    Passenger,
    Reservation
)
from django.contrib import admin


@register(Portal)
class PortalAdmin(ModelAdmin):
    """
    Admin configuration for the Portal model.
    """
    list_display = (
        "id",
        "name",
        "email",
        "theme_color",
        "is_active",
    )

    list_display_links = ("name",)
    search_fields = ("name",)
    search_help_text = _("Search by name")
    show_full_result_count = True
    list_per_page = 20

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


@register(SocialMediaAccount)
class SocialMediaAccountAdmin(ModelAdmin):
    """
    Admin configuration for the SocialMediaAccount model.
    """
    list_display = (
        "portal",
        "name",
        "url",
        "description",
    )
    exclude = ('deleted_at',)
    list_display_links = ("name",)
    search_fields = ("name",)
    search_help_text = _("Search by name")
    show_full_result_count = True
    list_per_page = 20
    raw_id_fields = ("portal",)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


class TravelImageInline(TabularInline):
    """
    Inline configuration for the TravelImage model.
    """
    exclude = ('deleted_at',)
    model = TravelImage
    extra = 1


class TravelDestinationInline(TabularInline):
    """
    Inline configuration for the TravelDestination model.
    """
    exclude = ('deleted_at',)
    model = TravelDestination
    extra = 1


@register(Travel)
class TravelAdmin(ModelAdmin, DynamicArrayMixin):
    """
    Admin configuration for the Travel model.
    """
    list_display = (
        "name", "start_date", "end_date", "is_active", "max_passengers", "total_reserved", "is_capacity_full", "cancelled"
    )
    list_display_links = ("name",)
    show_full_result_count = True
    list_per_page = 20
    exclude = ('deleted_at',)
    search_fields = ("name",)
    search_help_text = _("Search by name")
    formfield_overrides = {
        DynamicArrayField: {'widget': DynamicArrayTextareaWidget},
    }
    inlines = [
        TravelImageInline,
        TravelDestinationInline,
    ]

    @admin.display(description="Total Reserved")
    def total_reserved(self, obj):
        """docstring total_reserved"""
        total = Reservation.objects.filter(
            travel=obj,
            booking_confirmed=True
        ).count()
        return total


class ReservationInline(TabularInline):
    """
    Inline configuration for the Reservation model.
    """
    exclude = ('deleted_at',)
    raw_id_fields = (
        "travel",
        "passenger"
    )
    model = Reservation
    extra = 1


@register(Passenger)
class PassengerAdmin(ModelAdmin):
    show_full_result_count = True
    list_per_page = 20
    exclude = ('deleted_at',)
    search_fields = ("first_name", "last_name")
    search_help_text = _("Search by name")
    inlines = [
        ReservationInline,
    ]
    list_display = (
        "first_name", "last_name", "phone", "email"
    )
