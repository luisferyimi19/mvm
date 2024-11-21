import uuid as uuid_lib

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from apps.authentication.constants import AuthenticationManagementConstants


class UserManager(BaseUserManager):
    """docstring for UserManager"""

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError(AuthenticationManagementConstants.THE_GIVEN_EMAIL_MUST_BE_SET)
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        extra_fields.setdefault(AuthenticationManagementConstants.IS_STAFF, False)
        extra_fields.setdefault(AuthenticationManagementConstants.IS_SUPERUSER, False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email, and password.
        """
        extra_fields.setdefault(AuthenticationManagementConstants.IS_STAFF, True)
        extra_fields.setdefault(AuthenticationManagementConstants.IS_SUPERUSER, True)

        if extra_fields.get(AuthenticationManagementConstants.IS_STAFF) is not True:
            raise ValueError(AuthenticationManagementConstants.SUPERUSER_MUST_HAVE_IS_STAFF)
        if extra_fields.get(AuthenticationManagementConstants.IS_SUPERUSER) is not True:
            raise ValueError(AuthenticationManagementConstants.SUPERUSER_MUST_HAVE_IS_SUPERUSER)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """docstring for User"""

    id = models.BigAutoField(
        primary_key=True,
        editable=False,
        db_column=AuthenticationManagementConstants.ID,
    )
    uuid = models.UUIDField(
        verbose_name=AuthenticationManagementConstants.UUID,
        db_column=AuthenticationManagementConstants.UUID,
        default=uuid_lib.uuid4,
        unique=True,
        editable=False,
    )
    email = models.EmailField(
        verbose_name=AuthenticationManagementConstants.EMAIL_ADDRESS,
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=AuthenticationManagementConstants.FIRST_NAME,
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name=AuthenticationManagementConstants.LAST_NAME,
        max_length=150,
        blank=True
    )
    is_staff = models.BooleanField(
        verbose_name=AuthenticationManagementConstants.STAFF_STATUS,
        default=False,
        help_text=AuthenticationManagementConstants.DESIGNATES_WHETHER_THE_USER_CAN_LOG_INTO_THIS_ADMIN_SITE,
    )
    is_active = models.BooleanField(
        verbose_name=AuthenticationManagementConstants.ACTIVE,
        default=True,
        help_text=AuthenticationManagementConstants.DESIGNATES_WHETHER_THIS_USER_SHOULD_BE_TREATED_AS_ACTIVE,
    )
    date_joined = models.DateTimeField(AuthenticationManagementConstants.DATE_JOINED, default=timezone.now)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=AuthenticationManagementConstants.GROUPS,
        blank=True,
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=AuthenticationManagementConstants.USER_PERMISSIONS,
        blank=True,
        related_name='custom_user_set'
    )

    objects = UserManager()

    EMAIL_FIELD = AuthenticationManagementConstants.EMAIL
    USERNAME_FIELD = AuthenticationManagementConstants.EMAIL
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name.title()} {self.last_name.title()}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        app_label = "authentication"
        db_table = "authentication_users"
        ordering = [AuthenticationManagementConstants.EMAIL]
        verbose_name = "user"
        verbose_name_plural = "users"
