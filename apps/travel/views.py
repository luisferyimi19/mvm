from urllib.parse import quote_plus

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.functions import Concat, ExtractYear
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.db.models import OuterRef, Case, When, BooleanField, F, Value, CharField, ExpressionWrapper, IntegerField
from apps.travel.models import Travel, Reservation
from mvm.utils.subqueries import SubqueryCount
from django.utils import timezone
import itertools
from django.http import Http404, HttpResponseRedirect

from apps.travel.utils import get_portal_with_social_media_data, get_portal_data
from apps.authentication.models import User


class OverView(View):
    """
    OverView class based view
    """

    def get(self, request, *args, **kwargs):

        travels = Travel.objects.filter(
            cancelled=False,
            is_active=True,
            start_date__gt=timezone.now()
        ).annotate(
            passengers_count=SubqueryCount(
                Reservation.objects.filter(
                    travel__pk=OuterRef("pk"),
                    booking_confirmed=True,
                )
            ),
            is_travel_full=Case(
                When(
                    passengers_count__gte=F('max_passengers'), then=True
                ),
                When(
                    is_capacity_full=True, then=True
                ),
                default=False,
                output_field=BooleanField()
            ),
        ).order_by(
            "-start_date"
        )[:9]

        travels_data = travels.values(
            "uuid", "name", "start_date", "highlight_feature", "cover_image", "all_inclusive", "is_travel_full",
        )
        for travel in travels_data:
            travel["cover_image"] = settings.MEDIA_URL + str(travel["cover_image"])

        reviews_data = Reservation.objects.filter(
            review__isnull=False,
            booking_confirmed=True
        ).annotate(
            full_name=Concat(
                F("passenger__first_name"),
                Value(" "),
                F("passenger__last_name"),
                output_field=CharField(),
            ),
        ).values(
            "full_name", "review", "passenger__photo", "rating"
        )
        for review in reviews_data:
            review["photo"] = settings.MEDIA_URL + str(review["passenger__photo"])
            del review["passenger__photo"]

        portal_data = get_portal_with_social_media_data()
        data = {
            "travels": list(travels_data),
            "portal": portal_data["portal"],
            "social_media_accounts": portal_data["social_media_accounts"],
            "reviews": list(reviews_data)
        }
        return render(request, "travel/overview.html", data)


class TravelView(ListView):
    """
    TravelView class based view
    """
    model = Travel  # Set the model for the ListView
    template_name = 'travel/travels.html'  # Set the template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = get_portal_with_social_media_data()
        context["portal"] = data["portal"]
        context["social_media_accounts"] = data["social_media_accounts"]
        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            cancelled=False,
            is_active=True,
            start_date__gt=timezone.now()
        ).annotate(
            passengers_count=SubqueryCount(
                Reservation.objects.filter(
                    travel__pk=OuterRef("pk"),
                    booking_confirmed=True,
                )
            ),
            is_travel_full=Case(
                When(
                    passengers_count__gte=F('max_passengers'), then=True
                ),
                When(
                    is_capacity_full=True, then=True
                ),
                default=False,
                output_field=BooleanField()
            ),
            year=ExpressionWrapper(ExtractYear("start_date"), output_field=IntegerField())
        ).order_by("-start_date")

    def render_to_response(self, context, **response_kwargs):
        travels_data = context["object_list"].values(
            "uuid", "name", "start_date", "highlight_feature", "cover_image", "all_inclusive", "is_travel_full", "year"
        )
        travels_data_sorted = sorted(travels_data, key=lambda x: x["year"])
        travels_data_grouped = {}
        for year, group in itertools.groupby(travels_data_sorted, key=lambda x: x["year"]):
            travels_data_grouped[year] = list(group)
        travels_data_grouped = {k: travels_data_grouped[k] for k in sorted(travels_data_grouped.keys(), reverse=True)}

        years = sorted(set(travel["year"] for travel in travels_data), reverse=True)
        for travel in travels_data:
            travel["cover_image"] = settings.MEDIA_URL + str(travel["cover_image"])

        data = {
            "travels": travels_data_grouped,
            "years": years,
            "portal": context["portal"],
            "social_media_accounts": context["social_media_accounts"],
        }
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=data,
            **response_kwargs
        )


class TravelDetailView(DetailView):
    """
    TravelDetailView class based view
    """
    model = Travel
    template_name = 'travel/details.html'
    not_found_template = 'travel/detail_not_found.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'travel_uuid'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            cancelled=False,
            is_active=True,
            start_date__gt=timezone.now()
        ).annotate(
            passengers_count=SubqueryCount(
                Reservation.objects.filter(
                    travel__pk=OuterRef("pk"),
                    booking_confirmed=True,
                )
            ),
            is_travel_full=Case(
                When(
                    passengers_count__gte=F('max_passengers'), then=True
                ),
                When(
                    is_capacity_full=True, then=True
                ),
                default=False,
                output_field=BooleanField()
            ),
        ).prefetch_related(
            "travel_images",
            "travel_destinations",
        ).order_by(
            "-start_date"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        travel = self.get_object()

        start_date = travel.start_date.strftime("%d de %B")
        end_date = travel.end_date.strftime("%d de %B")
        date_range = f"Del {start_date} al {end_date}"

        travel_data = {
            "uuid": str(travel.uuid),
            "name": travel.name,
            "date": date_range,
            "description": travel.description,
            "highlight_feature": travel.highlight_feature,
            "cover_image": settings.MEDIA_URL + str(travel.cover_image),
            "counter": travel.max_passengers - travel.passengers_count,
            "inclusions": travel.inclusions,
            "restrictions": travel.restrictions,
            "all_inclusive": travel.all_inclusive,
            "is_travel_full": travel.is_travel_full,
            "travel_images": [],
            "travel_destinations": [],
        }

        travel_images = list(travel.travel_images.values("image"))
        for travel_image in travel_images:
            travel_data["travel_images"].append(
                settings.MEDIA_URL + str(travel_image.get("image"))
            )

        travel_destinations = list(travel.travel_destinations.order_by(
            "start_date"
        ).values("name", "image", "start_date", "end_date", "description"))

        for travel_destination in travel_destinations:
            start_date = travel_destination.get("start_date").strftime("%d")
            end_date = travel_destination.get("end_date").strftime("%d de %B")
            date_range = f"Del {start_date} al {end_date}"

            travel_data["travel_destinations"].append(
                {
                    "name": travel_destination.get("name"),
                    "date": date_range,
                    "image": settings.MEDIA_URL + str(travel_destination.get("image")),
                    "description": travel_destination.get("description", None)
                }
            )

        portal_data = get_portal_with_social_media_data()

        context["travel"] = travel_data
        context["portal"] = portal_data["portal"]
        context["social_media_accounts"] = portal_data["social_media_accounts"]
        print(context)
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            context = get_portal_with_social_media_data()
            context["reason"] = "Viaje no disponible"
            return render(request, self.not_found_template, context)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class GalleryView(ListView):
    """
    GalleryView class based view
    """
    model = Travel  # Set the model for the ListView
    template_name = 'travel/gallery.html'  # Set the template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = get_portal_with_social_media_data()
        context["portal"] = data["portal"]
        context["social_media_accounts"] = data["social_media_accounts"]
        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            cancelled=False,
            end_date__lt=timezone.now()
        ).annotate(
            year=ExpressionWrapper(ExtractYear("start_date"), output_field=IntegerField())
        )

    def render_to_response(self, context, **response_kwargs):
        travels_data = context["object_list"].values(
            "uuid", "name", "start_date", "cover_image", "year"
        )
        travels_data_sorted = sorted(travels_data, key=lambda x: x["year"])
        travels_data_grouped = {}
        for year, group in itertools.groupby(travels_data_sorted, key=lambda x: x["year"]):
            travels_data_grouped[year] = list(group)
        travels_data_grouped = {k: travels_data_grouped[k] for k in sorted(travels_data_grouped.keys(), reverse=True)}

        years = sorted(set(travel["year"] for travel in travels_data), reverse=True)
        for travel in travels_data:
            travel["cover_image"] = settings.MEDIA_URL + str(travel["cover_image"])

        data = {
            "travels": travels_data_grouped,
            "years": years,
            "portal": context["portal"],
            "social_media_accounts": context["social_media_accounts"],
        }
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=data,
            **response_kwargs
        )


class TravelGalleryView(DetailView):
    """
    TravelGalleryView class based view
    """
    model = Travel
    template_name = 'travel/travel_galery.html'
    not_found_template = 'travel/detail_not_found.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'travel_uuid'

    def get_queryset(self):
        return super().get_queryset().filter(
            cancelled=False,
            end_date__lt=timezone.now()
        ).annotate(
            year=ExpressionWrapper(ExtractYear("start_date"), output_field=IntegerField())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        travel = self.get_object()

        start_date = travel.start_date.strftime("%d de %B de %Y")

        travel_data = {
            "uuid": str(travel.uuid),
            "name": travel.name,
            "start_date": start_date,
            "cover_image": settings.MEDIA_URL + str(travel.cover_image),
            "travel_images": [],
            "url": travel.url
        }

        travel_images = list(travel.travel_images.filter(is_gallery_image=True).values("image"))
        for travel_image in travel_images:
            travel_data["travel_images"].append(
                settings.MEDIA_URL + str(travel_image.get("image"))
            )
        travel_data["travel_images"] = [travel_data["travel_images"][i::3] for i in range(3)]

        portal_data = get_portal_with_social_media_data()
        context["travel"] = travel_data
        context["portal"] = portal_data["portal"]
        context["social_media_accounts"] = portal_data["social_media_accounts"]
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if not self.object.travel_images.filter(is_gallery_image=True).exists() and not self.object.url:
                raise Http404
        except Http404:
            context = get_portal_with_social_media_data()
            context["reason"] = "Oops! Imagenes no se han cargado"
            return render(request, self.not_found_template, context)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class WhatsappTravelView(DetailView):
    """
    View to send information about a travel via WhatsApp.

    This view redirects the user to WhatsApp with a predefined message
    that includes the name of the travel and the URL of the previous page.

    Args:
        request (HttpRequest): The received HTTP request.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        HttpResponseRedirect: Redirects the user to WhatsApp.
    """
    model = Travel
    slug_field = 'uuid'
    slug_url_kwarg = 'travel_uuid'

    def get(self, request, *args, **kwargs):
        """
        GET method to process the HTTP request.

        Args:
            request (HttpRequest): The received HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponseRedirect: Redirects the user to WhatsApp.
        """
        # Get the travel object
        instance = self.get_object()

        # Get portal info
        portal = get_portal_data()

        # Get the full URL of the previous page
        referer_url = request.META.get('HTTP_REFERER', '')

        # Construct the message for WhatsApp
        message = (
            "Hola,\n\n"
            f"Estoy interesada en más información sobre el viaje {instance.name}.\n\n"
            f"{referer_url}\n\n"
            "¡Gracias!"
        )

        # Construct the WhatsApp URL with the encoded message
        url_whatsapp = f"https://wa.me/502{portal.mobile_phone}?text={quote_plus(message)}"

        # Redirect the user to WhatsApp
        return HttpResponseRedirect(url_whatsapp)


class WhatsappGeneralView(View):
    """
    View for redirecting users to WhatsApp to inquire about upcoming trips.

    This view constructs a message asking if the user would like information about
    upcoming trips and redirects the user to WhatsApp with the pre-defined message.

    Attributes:
        model: The model associated with the view.
        slug_field: The field used for looking up the model by its slug.
        slug_url_kwarg: The URL keyword argument that contains the slug.

    Methods:
        get: Processes the HTTP GET request to generate and redirect with the WhatsApp message.

    Returns:
        HttpResponseRedirect: Redirects the user to WhatsApp with the pre-defined message.
    """

    model = Travel
    slug_field = 'uuid'
    slug_url_kwarg = 'travel_uuid'

    def get(self, request, *args, **kwargs):
        """
        Process the HTTP GET request to generate and redirect with the WhatsApp message.

        Args:
            request (HttpRequest): The received HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponseRedirect: Redirects the user to WhatsApp with the pre-defined message.
        """
        # Construct the message for WhatsApp
        message = "Hola, ¿Quisiera información de sus próximos viajes?"

        # Construct the WhatsApp URL with the encoded message
        url_whatsapp = f"https://wa.me/50233570444?text={quote_plus(message)}"

        # Redirect the user to WhatsApp
        return HttpResponseRedirect(url_whatsapp)


class ContactView(View):

    model = Travel  # Set the model for the ListView
    template_name = 'contact.html'  # Set the template name

    def get(self, request, *args, **kwargs):
        portal_data = get_portal_with_social_media_data()
        data = {
            "portal": portal_data["portal"],
            "social_media_accounts": portal_data["social_media_accounts"],
        }
        return render(request, "contact.html", data)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        message = (f"Nombre: {name} \n\n"
                   f"Correo: {email} \n\n"
                   f"Mensaje: {message}")

        recipient_list = list(
            User.objects.all().values_list("email", flat=True)
        )

        # Envía el correo electrónico
        send_mail(
            subject,  # Asunto del correo
            message,  # Cuerpo del correo
            settings.EMAIL_HOST_USER,  # Dirección de correo electrónico del remitente (configurada en settings.py)
            recipient_list,
            # Lista de destinatarios (puedes usar una dirección de correo electrónico o una lista de ellas)
            fail_silently=False,  # Indica si se debe elevar una excepción en caso de error al enviar el correo
        )

        portal_data = get_portal_with_social_media_data()
        data = {
            "portal": portal_data["portal"],
            "social_media_accounts": portal_data["social_media_accounts"],
        }
        return render(request, "contact.html", data)


def no_found_handle(request, exception):
    context = get_portal_with_social_media_data()
    context["reason"] = "No se encontraron resultados"
    return render(request, 'travel/detail_not_found.html', context)