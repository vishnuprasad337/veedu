from django.contrib import admin
from .models import User, Hotel, Room, RoomNumber, Hotelbooking, ConnectionRequest

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomNumber)
admin.site.register(Hotelbooking)
admin.site.register(ConnectionRequest)
from django.contrib import admin
from django.conf import settings
import requests


@admin.action(description="Approve connection")
def approve_connection(modeladmin, request, queryset):

    for obj in queryset:

        api_key = settings.MY_API_KEY

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
                timeout=5
            )
        except:
            pass
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['hotel_name', 'status', 'callback_url', 'created_at']  
    actions = [approve_connection]   