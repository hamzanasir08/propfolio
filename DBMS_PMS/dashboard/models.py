
from django.db import models
from django.conf import settings  # To reference the CustomUser model from another app
from userReg.models import CustomUser

class City(models.Model):
    cityID = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)

    def __str__(self):
        return self.city_name

class Town(models.Model):
    townID = models.AutoField(primary_key=True)
    town_name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='towns')

    def __str__(self):
        return self.town_name



class Image(models.Model):
    imageID = models.AutoField(primary_key=True)
    images = models.ImageField(upload_to='property_images/')  # You can specify the upload directory

class Property(models.Model):
    posted_on = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created
    facing = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    description = models.TextField(max_length=1000)
    sale_type = models.CharField(max_length=50)
    images = models.ManyToManyField(Image)  # Assuming a property can have multiple images
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}, {self.city.city_name}"
    

class Appointment(models.Model):
    appointment_ID = models.AutoField(primary_key=True)
    appointment_date_and_time = models.DateTimeField()
    visiting_user = models.ForeignKey(CustomUser, related_name='visiting_appointments', on_delete=models.CASCADE)
    propID = models.ForeignKey(Property, related_name='appointments', on_delete=models.CASCADE)
    userID = models.ForeignKey(CustomUser, related_name='user_appointments', on_delete=models.CASCADE)

    def __str__(self):
        return f"Appointment {self.appointment_ID} for Property {self.propID.address} with User {self.userID.username}"