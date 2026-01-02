from django.db import models
from django.contrib.auth.models import User


# Tourist (User Extension)
class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


# Tour Package
class Tour(models.Model):
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)

    def __str__(self):
        return self.title


# Booking
class Booking(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    persons = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist.user.username} - {self.tour.title}"