from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Hotel,Hotelbooking,Room
from django.db.models import Sum
from .serializers import UserSerializers,HotelSerializers,BookingSerializers,RoomSerializers,HotelDetailsSerializers
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from datetime import datetime
from django.conf import settings

class UserListCreateAPIView(APIView):
    def get(self,request):
        user=User.objects.all()
        serializer=UserSerializers(user,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer= UserSerializers(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class UserDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User not found"}, status=404)
        return Response(UserSerializers(user).data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "user not found"}, status=404)

        serializer = UserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not User:
            return Response({"error": "user not found"}, status=404)

        user.delete()
        return Response({"message": "Deleted"}, status=204)

class HotelRegisterAPIView(APIView):
    def get(self,request):
        hotel=Hotel.objects.all()
        serializers=HotelSerializers(hotel,many=True)
        return Response(serializers.data)
    def post(self,request):
        serializers=HotelSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data,status=201)
        return Response (serializers.errors,status=404)
    

        
        
class HotelListAPIView(APIView):
       def get_object(self,pk):
           try:
            return Hotel.objects.get(pk=pk)
           except Hotel.DoesNotExist:
            return None
           
       def get(self, request, pk):
        hotels = self.get_object(pk)
        if not hotels:
            return Response({"error": "hotel not found"}, status=404)
        return Response(HotelSerializers(hotels).data)
class RoomsAddAPIView(APIView):
   

    def get(self, request, pk):
        
        try:
            hotel = Hotel.objects.get(id=pk)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
        
       
        rooms = hotel.rooms.all()
        serializer = RoomSerializers(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        try:
            hotel = Hotel.objects.get(id=pk)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found"}, status=404)

        if not isinstance(request.data, list):
            return Response({"error": "Send list of rooms"}, status=400)

        updated_rooms = []

        for room_data in request.data:
            room_type = room_data.get("room_type")
            price = room_data.get("price")
            available_rooms = room_data.get("available_rooms", 0)
            existing_room=Room.objects.filter(hotel=hotel,room_type=room_type).first()
            if existing_room:
                existing_room.available_rooms += int(available_rooms)
                if price:
                    existing_room.price = price

                existing_room.save()

            
            else:
            
                serializer = RoomSerializers(data=room_data)
                if serializer.is_valid():
                    serializer.save(hotel=hotel)
                    updated_rooms.append(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
          
        return Response(updated_rooms, status=201)
                
             


class BookingregisterAPIView(APIView):
    def post(self,request):
        serializers=BookingSerializers(data=request.data)
        if serializers.is_valid():
            room=serializers.validated_data['rooms']
            count=serializers.validated_data['count']
            starting_date=serializers.validated_data['check_in']
            ending_date=serializers.validated_data['check_out']
            duration = (ending_date - starting_date).days
            days = max(duration, 1)

           
            if duration<=0:
                return Response ( {"error: check_out must be after check_in" },status=400)

           
            if room.available_rooms < count:
                 return Response(
                {"error": f"Only {room.available_rooms} rooms available"},status=status.HTTP_400_BAD_REQUEST)
           
            total_amount= days*room.price*count
                
            room.available_rooms-=count
            room.save()
            
            

            balance_rooms = room.available_rooms
            booking = serializers.save(balance_rooms=balance_rooms,total_amount=total_amount)

            result=BookingSerializers(booking).data

            return Response(result, status=status.HTTP_201_CREATED)
        return Response (serializers.errors,status=404)
  
    def get(self,request):
        booking=Hotelbooking.objects.all()
        serializers=BookingSerializers(booking,many=True)
        return Response(serializers.data)
   
class BookingListAPIView(APIView):  
    def get_object(self, pk):
        try:
            return Hotelbooking.objects.get(pk=pk)
        except Hotelbooking.DoesNotExist:
            return None
    def get(self, request, pk):
        booking = self.get_object(pk)
        if not booking:
            return Response({"error": "booking not found"}, status=404)

        return Response(BookingSerializers(booking).data)

class BookingListhotelAPI(APIView):
    def get(self, request, hotel_id):
        bookings = Hotelbooking.objects.filter(hotel_id=hotel_id)
        serializer = BookingSerializers(bookings, many=True)
        return Response(serializer.data)
    

class HotelFullAPIView(APIView):
    def get(self, request, pk):
        try:
            
            hotel = Hotel.objects.prefetch_related('rooms', 'hotelbooking_set').get(id=pk)
            serializer = HotelDetailsSerializers(hotel)
            return Response(serializer.data)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found"}, status=404)
class BookingAppFullAPIView(APIView):
    def get(self, request):
        api_key = request.headers.get('API-KEY')

        if api_key != settings.MY_API_KEY:
            return Response({"error": "Invalid API Key"}, status=403)

        hotels = Hotel.objects.prefetch_related('rooms', 'hotelbooking_set')
        serializer = HotelDetailsSerializers(hotels, many=True)
        return Response(serializer.data)


def index(request):
    return render(request, 'index.html')
def user(request):    
    return render(request, 'user.html')
def hotel(request):    
    return render(request, 'hotels.html')
def hotel_login_view(request):
    return render(request, "hotels_login.html")

def hotel_list_view(request):
    hotels = Hotel.objects.all()
    return render(request, "hotel_list.html", {"hotels": hotels})
def hotel_rooms_view(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = hotel.rooms.all()

    return render(request, 'hotel_rooms.html', {
        'hotel': hotel,
        'rooms': rooms
    })
def hotel_login_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            hotel = Hotel.objects.get(name=name, password=password)

            request.session['hotel_id'] = hotel.id

            return redirect('hotel_dashboard')

        except Hotel.DoesNotExist:
            return render(request, 'hotels_login.html', {
                'error': 'Invalid Hotel Name or Password'
            })

    return render(request, 'hotels_login.html')
  


def hotel_dashboard(request):
    hotel_id = request.session.get('hotel_id')

    if not hotel_id:
        return redirect('hotels_login')

    hotel = get_object_or_404(Hotel, id=hotel_id)

    return render(request, 'hotel_dashboard.html', {
        'hotel': hotel
    })
def hotel_rooms_dashboard(request):
    hotel_id = request.session.get('hotel_id')

    if not hotel_id:
        return redirect('hotels_login')

    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()

    return render(request, 'hotel_rooms_dashboard.html', {
        'hotel': hotel,
        'rooms': rooms
    })
def hotel_bookings_dashboard(request):
    hotel_id = request.session.get('hotel_id')

    if not hotel_id:
        return redirect('hotels_login')

    bookings = Hotelbooking.objects.filter(hotel_id=hotel_id)

    return render(request, 'hotel_booking_dashboard.html', {
        'bookings': bookings
    })
def room_adding_view(request,pk):
    hotel=get_object_or_404(Hotel,pk=pk)
    if request.method=='POST':
        rtype=request.POST.get('room_type')
        count=int(request.POST.get('count',1))
        room=Room.objects.filter(hotel=hotel,room_type=rtype).first()
        if room:
            room.available_rooms += count
           
            room.save()
        return redirect('hotel_room_dashboard',pk=pk)
    rooms = hotel.rooms.all()
    return render(request, 'hotel_rooms_dashboard.html', {
        'hotel': hotel, 
        'rooms': rooms
    })
    



def user_login(request):

    if request.method == "POST":
        email_input = request.POST.get('email').strip()
        password_input = request.POST.get('password').strip()

        try:
            user = User.objects.get(
                email=email_input,
                password=password_input
            )

            request.session['user_id'] = user.id
            return redirect('user_details')

        except User.DoesNotExist:
            return render(
                request,
                'user.html',
                {'error': 'Invalid Email or Password'}
            )

    return render(request, 'user.html')
def user_details(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('user_login')

    user = User.objects.get(id=user_id)   

    return render(
        request,
        'user_details.html',
        {'user': user}
    )
def hotel_details_view(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    return render(request,'hotel_details.html', {'hotel': hotel})


def process_booking(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        count = int(request.POST.get('count'))
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')

        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()

        if check_out < check_in:
            messages.error(request, "Check-out day should be after check-in")
            return render(request, 'booking.html', {'room': room})

        duration = (check_out - check_in).days
        days = max(duration, 1)

        if duration <= 0:
            messages.error(request, "Check-out must be after check-in.")
            return render(request, 'booking.html', {'room': room})

        if room.available_rooms < count:
            messages.error(request, f"Only {room.available_rooms} rooms available.")
            return render(request, 'booking.html', {'room': room})

        total_amount = days * float(room.price) * count

        try:
            user_instance = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered. Please signup before booking.")
            return render(request, 'booking.html', {'room': room})

       
        room.available_rooms -= count
        room.save()
        current_balance = room.available_rooms

        
        Hotelbooking.objects.create(
            user=user_instance,
            hotel=room.hotel,
            rooms=room,
            room_type=room.room_type,
            name=name,
            email=email,
            count=count,
            check_in=check_in,
            check_out=check_out,
            total_amount=total_amount,
            balance_rooms=current_balance
        )

        
        request.session['hotel_id'] = room.hotel.id

        messages.success(request, f"Booking successful! Total: ₹{total_amount}")
        return redirect('user_details')  

    return render(request, 'booking.html', {'room': room})
def signup(request):
    if request.method == "POST":
       
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phonenumber = request.POST.get("phonenumber")
        password = request.POST.get("password")

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return render(request, "signup.html")
        try:
            User.objects.create(
                user_name=user_name,
                email=email,
                Address=address, 
                phonenumber=phonenumber,
                password=password
            )
            
            messages.success(request, "Account created! You can now log in.")
            return redirect("hotel_list")  

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, "signup.html")

    
    return render(request, "signup.html")

