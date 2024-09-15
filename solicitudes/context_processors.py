from django.conf import settings

def global_settings(request):
    return {
        'API_URL': settings.API_URL
    }