from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CharField,
    EmailField,
    ImageField,
    TextField,
    ForeignKey,
    CASCADE,
    DateField,
    BooleanField,
    PositiveIntegerField,
    IntegerField
)
from spectrum.fields import ColorField
from apps.travel.constants import TravelManagementConstants
from apps.general.models import CommonInfo
from django_better_admin_arrayfield.models.fields import ArrayField


class Portal(CommonInfo):
    """
    Represents a portal for travel management.

    Attributes:
        name (CharField): The name of the portal.
        address (CharField): The address of the portal.
        email (EmailField): The email address of the portal.
        mobile_phone (CharField): The mobile phone number of the portal.
        theme_color (ColorField): The theme color of the portal.
        is_active (BooleanField): Indicates if the portal is active.
    """
    name = CharField(
        unique=True,
        verbose_name=TravelManagementConstants.NAME,
        help_text=TravelManagementConstants.NAME,
        db_column="name",
        max_length=255,
    )
    address = CharField(
        verbose_name=TravelManagementConstants.ADDRESS,
        help_text=TravelManagementConstants.ADDRESS,
        db_column="address",
        max_length=255,
    )
    email = EmailField(
        verbose_name=TravelManagementConstants.EMAIL,
        max_length=255,
        db_column="email",
        help_text=TravelManagementConstants.EMAIL,
    )
    mobile_phone = CharField(
        verbose_name=TravelManagementConstants.MOBILE_PHONE,
        help_text=TravelManagementConstants.MOBILE_PHONE,
        db_column="mobile_phone",
        max_length=255,
    )
    theme_color = ColorField(
        verbose_name=TravelManagementConstants.THEME_COLOR,
        help_text=TravelManagementConstants.THEME_COLOR,
        db_column="theme_color",
        default="#fcccca",
        blank=True,
        null=True,
    )
    is_active = BooleanField(
        verbose_name=TravelManagementConstants.IS_ACTIVE,
        default=True,
        db_column="is_active",
        help_text=TravelManagementConstants.IS_ACTIVE,
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.name})"

    class Meta:
        app_label = "travel"
        db_table = "travel_portal"
        verbose_name = TravelManagementConstants.PORTAL
        verbose_name_plural = TravelManagementConstants.PORTALS
        ordering = ["name"]


class SocialMediaAccount(CommonInfo):
    """
    Represents a social media account associated with a portal.

    Attributes:
        portal (ForeignKey): The portal associated with the social media account.
        name (CharField): The name of the social media account.
        url (CharField): The URL of the social media account.
        description (TextField): The description of the social media account.
        is_active (BooleanField): Indicates if the social media account is active.
    """
    portal = ForeignKey(
        Portal,
        verbose_name=TravelManagementConstants.PORTAL,
        db_column="portal_id",
        on_delete=CASCADE,
        related_name="social_media_accounts",
        related_query_name="social_media_account",
        help_text=TravelManagementConstants.PORTAL,
    )
    name = CharField(
        unique=True,
        verbose_name=TravelManagementConstants.NAME,
        help_text=TravelManagementConstants.NAME,
        db_column="name",
        max_length=255,
    )
    url = CharField(
        verbose_name=TravelManagementConstants.URL,
        max_length=255,
        db_column="url",
        help_text=TravelManagementConstants.URL_OF_THE_SOCIAL_MEDIA_ACCOUNT
    )
    description = TextField(
        verbose_name=TravelManagementConstants.DESCRIPTION,
        help_text=TravelManagementConstants.DESCRIPTION,
        db_column="description",
        blank=True,
    )
    is_active = BooleanField(
        verbose_name=TravelManagementConstants.IS_ACTIVE,
        default=True,
        db_column="is_active",
        help_text=TravelManagementConstants.IS_ACTIVE,
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.name})"

    class Meta:
        app_label = "travel"
        db_table = "travel_social_media_account"
        ordering = ["name"]
        verbose_name = TravelManagementConstants.SOCIAL_MEDIA_ACCOUNT
        verbose_name_plural = TravelManagementConstants.SOCIAL_MEDIA_ACCOUNTS
        unique_together = [["name", "portal"]]


class Travel(CommonInfo):
    """
    Represents a travel.

    Attributes:
        name (CharField): The name of the travel.
        highlight_feature (CharField): The highlight feature of the travel.
        start_date (DateField): The start date of the travel.
        end_date (CharField): The end date of the travel.
        is_active (BooleanField): Indicates if the travel is active.
        all_inclusive (BooleanField): Indicates if the travel is all-inclusive.
        is_capacity_full (BooleanField): Indicates if the travel's capacity is full.
        cancelled (BooleanField): Indicates if the travel is cancelled.
        max_passengers (PositiveIntegerField): The maximum number of passengers for the travel.
        description (TextField): The description of the travel.
        cover_image (ImageField): The cover image of the travel.
        inclusions (ArrayField): The inclusions of the travel.
        restrictions (ArrayField): The restrictions of the travel.
    """
    name = CharField(
        verbose_name=TravelManagementConstants.NAME,
        help_text=TravelManagementConstants.NAME,
        db_column="name",
        max_length=255,
    )
    highlight_feature = CharField(
        verbose_name=TravelManagementConstants.HIGHLIGHT_FEATURE,
        help_text=TravelManagementConstants.HIGHLIGHT_FEATURE,
        db_column="highlight_feature",
        max_length=25,
        blank=True
    )
    start_date = DateField(
        verbose_name=TravelManagementConstants.START_DATE,
        help_text=TravelManagementConstants.START_DATE,
        db_column="start_date",
    )
    end_date = DateField(
        verbose_name=TravelManagementConstants.END_DATE,
        help_text=TravelManagementConstants.END_DATE,
        db_column="end_date",
    )
    is_active = BooleanField(
        verbose_name=TravelManagementConstants.IS_ACTIVE,
        default=True,
        db_column="is_active",
        help_text=TravelManagementConstants.IS_ACTIVE,
    )
    all_inclusive = BooleanField(
        verbose_name=TravelManagementConstants.ALL_INCLUSIVE,
        default=False,
        db_column="all_inclusive",
        help_text=TravelManagementConstants.ALL_INCLUSIVE,
    )
    is_capacity_full = BooleanField(
        verbose_name=TravelManagementConstants.IS_CAPACITY_FULL,
        default=False,
        db_column="is_capacity_full",
        help_text=TravelManagementConstants.IS_CAPACITY_FULL,
    )
    cancelled = BooleanField(
        verbose_name=TravelManagementConstants.CANCELLED,
        default=False,
        db_column="cancelled",
        help_text=TravelManagementConstants.CANCELLED,
    )
    max_passengers = PositiveIntegerField(
        verbose_name=TravelManagementConstants.MAX_PASSENGERS,
        default=1,
        db_column="max_passengers",
        help_text=TravelManagementConstants.MAX_PASSENGERS,
    )
    description = TextField(
        verbose_name=TravelManagementConstants.DESCRIPTION,
        help_text=TravelManagementConstants.DESCRIPTION,
        db_column="description",
    )
    cover_image = ImageField(
        verbose_name=TravelManagementConstants.COVER_IMAGE,
        help_text=TravelManagementConstants.COVER_IMAGE,
        db_column="cover_image",
        upload_to="travel/travels",
    )
    inclusions = ArrayField(
        CharField(
            max_length=500,
            blank=True,
            null=True
        ),
        verbose_name=TravelManagementConstants.INCLUSIONS,
        help_text=TravelManagementConstants.INCLUSIONS,
        size=10,
        blank=True,
        default=list,
        db_column="inclusions",
    )
    restrictions = ArrayField(
        CharField(
            max_length=500,
            blank=True,
            null=True
        ),
        verbose_name=TravelManagementConstants.RESTRICTIONS,
        help_text=TravelManagementConstants.RESTRICTIONS,
        size=10,
        blank=True,
        default=list,
        db_column="restrictions",
    )
    url = CharField(
        verbose_name=TravelManagementConstants.URL,
        max_length=255,
        db_column="url",
        help_text=TravelManagementConstants.URL_OF_THE_TRAVEL_IMAGES,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.name})"

    class Meta:
        app_label = "travel"
        db_table = "travel_travel"
        verbose_name = TravelManagementConstants.TRAVEL
        verbose_name_plural = TravelManagementConstants.TRAVELS
        ordering = ["-start_date"]


class TravelImage(CommonInfo):
    """
    Represents an image associated with a travel.

    Attributes:
        travel (ForeignKey): The travel associated with the image.
        image (ImageField): The image associated with the travel.
    """
    travel = ForeignKey(
        Travel,
        verbose_name=TravelManagementConstants.TRAVEL,
        db_column="travel_id",
        on_delete=CASCADE,
        related_name="travel_images",
        related_query_name="travel_image",
        help_text=TravelManagementConstants.TRAVEL,
    )
    image = ImageField(
        verbose_name=TravelManagementConstants.IMAGE,
        help_text=TravelManagementConstants.IMAGE,
        db_column="image",
        upload_to="travel/travel_images",
    )
    is_gallery_image = BooleanField(
        verbose_name=TravelManagementConstants.IS_GALLERY_IMAGE,
        default=False,
        db_column="is_gallery_image",
        help_text=TravelManagementConstants.IS_GALLERY_IMAGE,
    )

    class Meta:
        app_label = "travel"
        db_table = "travel_travel_image"
        verbose_name = TravelManagementConstants.TRAVEL
        verbose_name_plural = TravelManagementConstants.TRAVELS
        ordering = ["-id"]


class TravelDestination(CommonInfo):
    """
    Represents a destination associated with a travel.

    Attributes:
        travel (ForeignKey): The travel associated with the destination.
        name (CharField): The name of the destination.
        start_date (DateField): The start date of the destination.
        end_date (CharField): The end date of the destination.
        image (ImageField): The image associated with the destination.
        description (TextField): The description of the destination.
    """
    travel = ForeignKey(
        Travel,
        verbose_name=TravelManagementConstants.TRAVEL,
        db_column="travel_id",
        on_delete=CASCADE,
        related_name="travel_destinations",
        related_query_name="travel_destination",
        help_text=TravelManagementConstants.TRAVEL,
    )
    name = CharField(
        verbose_name=TravelManagementConstants.NAME,
        help_text=TravelManagementConstants.NAME,
        db_column="name",
        max_length=255,
    )
    start_date = DateField(
        TravelManagementConstants.START_DATE,
        help_text=TravelManagementConstants.START_DATE,
        db_column="start_date",
    )
    end_date = DateField(
        TravelManagementConstants.END_DATE,
        help_text=TravelManagementConstants.END_DATE,
        db_column="end_date",
    )
    image = ImageField(
        verbose_name=TravelManagementConstants.IMAGE,
        help_text=TravelManagementConstants.IMAGE,
        db_column="image",
        upload_to="travel/travel_destinations",
    )
    description = TextField(
        verbose_name=TravelManagementConstants.DESCRIPTION,
        help_text=TravelManagementConstants.DESCRIPTION,
        db_column="description",
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.name})"

    class Meta:
        app_label = "travel"
        db_table = "travel_travel_destination"
        verbose_name = TravelManagementConstants.TRAVEL_DESTINATION
        verbose_name_plural = TravelManagementConstants.TRAVEL_DESTINATIONS
        ordering = ["-start_date"]


class Passenger(CommonInfo):
    """
    Represents a passenger for a travel.

    Attributes:
        first_name (CharField): The first name of the passenger.
        last_name (CharField): The last name of the passenger.
        phone (CharField): The phone number of the passenger.
        email (EmailField): The email address of the passenger.
    """
    first_name = CharField(
        TravelManagementConstants.FIRST_NAME,
        db_column="first_name",
        help_text=TravelManagementConstants.FIRST_NAME,
        max_length=250,
    )
    last_name = CharField(
        TravelManagementConstants.LAST_NAME,
        db_column="last_name",
        help_text=TravelManagementConstants.LAST_NAME,
        max_length=250
    )
    phone = CharField(
        TravelManagementConstants.PHONE,
        max_length=255,
        db_column="phone",
        blank=True,
        help_text=TravelManagementConstants.PHONE,
    )
    email = EmailField(
        verbose_name=TravelManagementConstants.EMAIL,
        max_length=255,
        db_column="email",
        help_text=TravelManagementConstants.EMAIL,
        null=True,
        blank=True,
    )
    photo = ImageField(
        verbose_name=TravelManagementConstants.PHOTO,
        help_text=TravelManagementConstants.PHOTO,
        db_column="photo",
        upload_to="travel/passengers",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.first_name} {self.last_name})"

    class Meta:
        app_label = "travel"
        db_table = "travel_passenger"
        verbose_name = TravelManagementConstants.PASSENGER
        verbose_name_plural = TravelManagementConstants.PASSENGERS
        ordering = ["first_name", "last_name"]


class Reservation(CommonInfo):
    """
    Represents a reservation for a travel.

    Attributes:
        travel (ForeignKey): The travel associated with the reservation.
        passenger (ForeignKey): The passenger associated with the reservation.
        review (TextField): The review of the travel.
        booking_confirmed (BooleanField): Indicates if the booking for the reservation is confirmed.
    """
    travel = ForeignKey(
        Travel,
        verbose_name=TravelManagementConstants.TRAVEL,
        db_column="travel_id",
        on_delete=CASCADE,
        related_name="reservation_travels",
        related_query_name="reservation_travel",
        help_text=TravelManagementConstants.TRAVEL,
    )
    passenger = ForeignKey(
        Passenger,
        verbose_name=TravelManagementConstants.PASSENGER,
        db_column="passenger_id",
        on_delete=CASCADE,
        related_name="reservation_passengers",
        related_query_name="reservation_passenger",
        help_text=TravelManagementConstants.PASSENGER,
    )
    review = TextField(
        verbose_name=TravelManagementConstants.REVIEW,
        help_text=TravelManagementConstants.REVIEW,
        db_column="review",
        blank=True,
    )
    booking_confirmed = BooleanField(
        verbose_name=TravelManagementConstants.BOOKING_CONFIRMED,
        default=False,
        db_column="booking_confirmed",
        help_text=TravelManagementConstants.BOOKING_CONFIRMED,
    )
    rating = IntegerField(
        verbose_name=TravelManagementConstants.RATING,
        default=0,
        help_text=TravelManagementConstants.TRAVEL_RATING,
        db_column="rating",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    def __str__(self):
        return f"{self.booking_confirmed}"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.booking_confirmed})"

    class Meta:
        app_label = "travel"
        db_table = "travel_reservation"
        verbose_name = TravelManagementConstants.RESERVATION
        verbose_name_plural = TravelManagementConstants.RESERVATIONS
        unique_together = [["travel", "passenger"]]
