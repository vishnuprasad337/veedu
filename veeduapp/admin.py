from django.contrib import admin
from django.conf import settings
import requests

from .models import User, Hotel, Room, RoomNumber, Hotelbooking, ConnectionRequest


admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomNumber)
admin.site.register(Hotelbooking)


@admin.action(description="Approve connection")
def approve_connection(modeladmin, request, queryset):
    for obj in queryset:
       
        api_key = getattr(settings, 'MY_API_KEY', 'default_key_123')

        obj.api_key = api_key
        obj.status = "approved"
        obj.save()

        try:
            requests.post(
                obj.callback_url,
                json={
                    "website": "Veedu",
                    "hotel_name": obj.hotel_name,
                    "api_key": api_key
                },
                timeout=10
            )
        except Exception as e:
            print(f"Callback failed: {e}")


class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['hotel_name', 'status']
    actions = [approve_connection]


admin.site.register(ConnectionRequest, ConnectionRequestAdmin)