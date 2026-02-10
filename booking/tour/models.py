from django.db import models
from django.contrib.auth.models import User

# Tourist (User extension)
class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=10, unique=True)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name or self.user.username


class Tour(models.Model):
    title = models.CharField(max_length=200)   # Mustang Tour Package
    destination = models.CharField(max_length=150)

    duration_days = models.PositiveIntegerField()
    base_price = models.PositiveIntegerField(help_text="Price for 1 person")

    description = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_price(self, persons):
        if persons == 1:
            return self.base_price
        elif persons == 2:
            return int(self.base_price * 1.8)
        else:
            return int(self.base_price * persons * 0.85)

    def __str__(self):
        return self.title

class TourPlace(models.Model):
    tour = models.ForeignKey(
        Tour,
        related_name='places',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)  # Muktinath Temple
    description = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.tour.title})"

class TourImage(models.Model):
    tour = models.ForeignKey(
        Tour,
        related_name='images',
        on_delete=models.CASCADE
    )

    image = models.ImageField(upload_to='tours/')

    def __str__(self):
        return f"Image for {self.tour.title}"



# Optional Hotel (for packages)
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    price_per_day = models.PositiveIntegerField()
    hotel_image = models.ImageField(upload_to='hotels/', blank=True, null=True)

    def __str__(self):
        return self.name


# Optional Add-ons (hike, city tour, etc.)
class Addon(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()  # fixed price per addon

    def __str__(self):
        return self.name


# Booking
# models.py

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    addons = models.ManyToManyField(Addon, blank=True)
    days = models.PositiveIntegerField(default=1)
    persons = models.PositiveIntegerField(default=1)  # add persons if not already
    total_price = models.PositiveIntegerField(default=0)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.tourist.user.username} - {self.tour.title}"

    @property
    def computed_total_price(self):
        """Dynamic total price calculation"""
        price = self.tour.base_price * self.days

        # Discount based on days
        if self.days == 2:
            price *= 0.9
        elif self.days >= 3:
            price *= 0.85

        # Hotel cost
        if self.hotel:
            price += self.hotel.price_per_day * self.days

        # Addons
        if self.addons.exists():
            for addon in self.addons.all():
                price += addon.price

        # Multiply by persons
        return int(price * self.persons)


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('offline', 'Offline'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='esewa')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.booking.id} - {self.status}"

