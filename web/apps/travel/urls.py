from django.urls import path
from apps.travel.views import OverView, TravelView, TravelDetailView, GalleryView, TravelGalleryView, \
    WhatsappGeneralView, WhatsappTravelView, ContactView

urlpatterns = [
    path("", OverView.as_view(), name="overview"),
    path("travels/", TravelView.as_view(), name="my-travels"),
    path('travel-details/<uuid:travel_uuid>/', TravelDetailView.as_view(), name='travel_details'),
    path('whatsapp-travel/<uuid:travel_uuid>/', WhatsappTravelView.as_view(), name='whatsapp_travel'),
    path('whatsapp-general/', WhatsappGeneralView.as_view(), name='whatsapp-general'),
    path("gallery/", GalleryView.as_view(), name="gallery"),
    path('travel-gallery/<uuid:travel_uuid>/', TravelGalleryView.as_view(), name='travel_gallery'),
    path("contact/", ContactView.as_view(), name="contact"),
]