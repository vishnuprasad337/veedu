from django.urls import path
from .views import *
urlpatterns=[

    path('', index, name='home'),
    path('user/login/', user_login, name='user_login'),
    path('user/details/', user_details, name='user_details'),
    path('user/signup/', signup, name='signup'),
    
    path('user', user, name='user'),
    path('hotel/', hotel, name='hotel'),
    path('hotel/login/', hotel_login_view, name='hotel_login'),
    path('hotel/list/', hotel_list_view, name='hotel_list'),
    path('hotel/<int:pk>/rooms/', hotel_rooms_view, name='hotel_rooms'),
    path('hotel/login/', hotel_login_view, name='hotel_login'),
    path('hotel/dashboard/',  hotel_dashboard, name='hotel_dashboard'),
  # path('hotel/logout/', views.hotel_logout, name='hotel_logout'),
    path('hotel/dashboard/rooms/', hotel_rooms_dashboard, name='hotel_rooms_dashboard'),
    path('hotel/dashboard/bookings/',hotel_bookings_dashboard, name='hotel_bookings_dashboard'),
    path('hotel/<int:pk>/rooms/', room_adding_view, name='hotel_rooms_dashboard'),
    path('hotel/<int:pk>/details/',hotel_details_view, name='hotel_details'),
    path('hotel/<int:pk>/book/',process_booking, name='process_booking'),
    
    
    
    
    
    
    
    path('api/users/', UserListCreateAPIView.as_view()),
    path('api/users/<int:pk>/', UserDetailsAPIView.as_view()),
    path('api/hotels/', HotelRegisterAPIView.as_view()),
    path('api/hotels/<int:pk>/',  HotelListAPIView.as_view()),
    path('api/hotels/<int:pk>/rooms',  RoomsAddAPIView.as_view()),
    path('api/hotels/booking/', BookingregisterAPIView.as_view()),
    path('api/hotels/booking/<int:pk>/', BookingListAPIView .as_view()),
    path('api/hotels/<int:hotel_id>/bookings/', BookingListhotelAPI.as_view()),
    path('hotel/<int:pk>/all/', HotelFullAPIView.as_view()),
    path('bookingapp/api/', BookingAppFullAPIView.as_view()),

    
]

