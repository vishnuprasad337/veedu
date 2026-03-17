from django.contrib import admin
from django.conf import settings
import requests
# Import all your models
from .models import User, Hotel, Room, RoomNumber, Hotelbooking, ConnectionRequest

# 1. Register standard models
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


class ConnectionRequestAdmin(admin.ModelAdmin):# Ensure 'created_at' exists in your models.py, otherwise remove it from this list
    list_display = ['hotel_name', 'status', 'callback_url'] 
    actions = [approve_connection]


admin.site.register(ConnectionRequest, ConnectionRequestAdmin)