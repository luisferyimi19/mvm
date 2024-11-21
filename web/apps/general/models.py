import uuid
from django.db.models import Model, UUIDField, DateTimeField, BigAutoField
from apps.general.constants import GeneralManagementConstants


class CommonInfo(Model):
    """docstring for CommonInfo"""

    id = BigAutoField(
        primary_key=True,
        editable=False,
        db_column="id",
    )
    uuid = UUIDField(
        verbose_name= GeneralManagementConstants.UUID,
        db_column="uuid",
        default=uuid.uuid4,
        db_index=True,
        unique=True,
        editable=False,
    )
    created_at = DateTimeField(
        verbose_name= GeneralManagementConstants.CREATED_AT,
        auto_now_add=True,
        db_column="created_at",
        db_index=True,
        help_text= GeneralManagementConstants.CREATED_AT,
    )

    updated_at = DateTimeField(
        verbose_name= GeneralManagementConstants.UPDATED_AT,
        auto_now=True,
        null=True,
        blank=True,
        db_column="updated_at",
        help_text= GeneralManagementConstants.UPDATED_AT,
    )

    deleted_at = DateTimeField(
        verbose_name= GeneralManagementConstants.DELETED_AT,
        null=True,
        blank=True,
        db_column="deleted_at",
        help_text= GeneralManagementConstants.DELETED_AT,
    )

    class Meta:
        abstract = True
