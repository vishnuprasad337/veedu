from rest_framework import serializers
from .models import User,Hotel,Hotelbooking,Room,RoomNumber


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model =User
        model = User
        fields = ['id', 'user_name', 'Address', 'email', 'phonenumber', 'password']
        extra_kwargs = {
            'password': {'write_only': True} 
        }
class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model =Hotel
        fields = ['id', 'name', 'city', 'hotel_type', 'password']
        extra_kwargs = {
            'password': {'write_only': True} 
            
        }
class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields=  fields = ['id','room_type', 'price', 'available_rooms','total_rooms']
       ## read_only_fields=['hotel']


   
class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotelbooking
        fields = [
            'id', 'hotel', 'rooms', 'room_type', 'name', 'email',
            'count', 'check_in', 'check_out', 'is_available', 'balance_rooms','total_amount'

        ]

class HotelDetailsSerializers(serializers.ModelSerializer):
    
    rooms = RoomSerializers(many=True, read_only=True)
    bookings = BookingSerializers(many=True, read_only=True,source='hotelbooking_set')

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'city', 'hotel_type', 'rooms', 'bookings']
  
    
    
