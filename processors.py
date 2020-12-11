from message.models import Message
from django.conf import settings

def message_count(request):
    new_message_count=None
    if request.user.is_authenticated:
        new_message_count = Message.objects.filter(
            consumer=request.user,
            new=True
        ).count()

    return {"new_message_count":new_message_count}

def get_google_map_api_key(request):
    return {"google_map_api_key":settings.GOOGLE_MAPS_API_KEY}
