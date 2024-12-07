from django.contrib import admin
from bookings import models

admin.site.register(models.Train)
admin.site.register(models.Seat)
admin.site.register(models.Booking)