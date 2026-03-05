from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits."
    )


    user_name=  models.CharField(max_length=100)
    Address= models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phonenumber=models.CharField(validators=[phone_validator])
    created_at =models.DateTimeField(auto_now_add=True)
    password=models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user_name}  {self.email}"
    
    


class Hotel(models.Model):

   
    name=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    hotel_type = models.CharField(max_length=100)
    password = models.CharField(max_length=128,default=0)

    def __str__(self):
        return self.name
    
class Room(models.Model):
     ROOM_CHOICES = (
        ('Normal', 'Normal'),
        ('2 star', '2 star'),
        ('5 star', '5 star'),
        ('delux', 'delux'),
    )
    
     hotel =models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='rooms')
     
     room_type = models.CharField(max_length=100, choices=ROOM_CHOICES , default='Normal')
     price = models.DecimalField(max_digits=10,decimal_places=2)
     total_rooms=models.IntegerField(default=0)
     available_rooms=models.IntegerField(default=0)
     is_available = models.BooleanField(default=True)

     def __str__(self):
         return f"{self.hotel.name} - {self.room_type}"
    
class RoomNumber(models.Model):
    room_category=models.ForeignKey(Room,on_delete=models.CASCADE)
    room_number=models.CharField(max_length=10,unique=True) 
    def __str__(self):
        return f"{self.room_number} - {self.room_category.room_type}"  
 

class Hotelbooking(models.Model):
    ROOM_CHOICES = (
        ('Normal', 'Normal'),
        ('2 star', '2 star'),
        ('5 star', '5 star'),
        ('delux', 'delux'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,default=1)
    rooms=models.ForeignKey(Room,on_delete=models.CASCADE,default=1)
    assigned_room = models.ForeignKey(RoomNumber, on_delete=models.SET_NULL, null=True)
    room_type=models.CharField(max_length=100, choices=ROOM_CHOICES , default='Normal')
    name =models.CharField(max_length=100)
    email = models.EmailField()
    count = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    is_available =models.BooleanField(default=True)
    balance_rooms=models.IntegerField(default=0)
    total_amount=models.DecimalField (max_digits=10,decimal_places=2,default=0)
    
    


    def __str__(self):
        return f"{self.name} {self.email}"

    
    
