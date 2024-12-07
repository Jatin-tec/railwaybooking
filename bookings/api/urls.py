from django.urls import path
from bookings.api import views

urlpatterns = [
    path('add-train', views.add_train, name='add_train'),
    path('get-trains', views.get_trains, name='get_trains'),
    path('book-seat', views.book_seat, name='book_seat'),
    path('get-booking/<int:booking_id>', views.get_booking, name='get_booking'),
]