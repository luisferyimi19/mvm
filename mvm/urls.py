"""mvm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.travel.urls import urlpatterns as urlpatterns_travel

urlpatterns = []

urlpatterns += (
    [
        path("admin/django-ses/", include("django_ses.urls")),
        # Auth urls
        path("auth/login/", auth_views.LoginView.as_view(), name="login"),
        path("auth/logout/", auth_views.LogoutView.as_view(), name="logout"),
        path(
            "auth/password_change/",
            auth_views.PasswordChangeView.as_view(),
            name="password_change",
        ),
        path(
            "auth/password_change/done/",
            auth_views.PasswordChangeDoneView.as_view(),
            name="password_change_done",
        ),
        path(
            "auth/password_reset/",
            auth_views.PasswordResetView.as_view(),
            name="admin_password_reset",
        ),
        path(
            "auth/password_reset/done/",
            auth_views.PasswordResetDoneView.as_view(),
            name="password_reset_done",
        ),
        path(
            "auth/reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(),
            name="password_reset_confirm",
        ),
        path(
            "auth/reset/done/",
            auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete",
        ),
        path(
            "",
            include(
                (urlpatterns_travel, "travels"),
                namespace="travels",
            ),
        ),
        path("admin/", admin.site.urls, name="admin"),
        path("__reload__/", include("django_browser_reload.urls")),

    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.index_title = "Bienvenidos a Mujeres Viajeras por el Mundo - Portal"

handler404 = "travel.views.no_found_handle"
