from apps.travel.models import Portal


def get_portal_data():
    portal = Portal.objects.filter(is_active=True).prefetch_related(
        "social_media_accounts"
    ).first()
    return portal

def get_portal_with_social_media_data():
    portal = get_portal_data()
    social_media_accounts = list(portal.social_media_accounts.values("name", "url"))
    data = {
        "portal": {
            "name": portal.name,
            "address": portal.address,
            "email": portal.email,
            "mobile_phone": portal.mobile_phone,
            "theme_color": portal.theme_color,
        },
        "social_media_accounts": social_media_accounts
    }
    return data
