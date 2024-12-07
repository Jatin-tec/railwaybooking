from django.db import models
from authentication.models import CustomUser as User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Train(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Seat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

@receiver(post_save, sender=Train)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.total_seats + 1):
            Seat.objects.create(train=instance, seat_number=f"Seat {i}")

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(default=datetime.now)
