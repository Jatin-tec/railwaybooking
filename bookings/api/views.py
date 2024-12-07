from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from bookings.models import Train
from django.db import transaction
from django.conf import settings

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_train(request):
    if request.headers.get('API-KEY') != settings.ADMIN_API_KEY:
        return Response({"error": "Unauthorized"}, status=HTTP_403_FORBIDDEN)
    
    data = request.data
    train = Train.objects.create(
        name=data['name'],
        source=data['source'],
        destination=data['destination'],
        total_seats=data['total_seats']
    )
    return Response({"message": "Train added successfully"})

@api_view(['GET'])
def get_trains(request):
    source = request.query_params.get('source')
    destination = request.query_params.get('destination')
    trains = Train.objects.filter(source=source, destination=destination)
    response = []
    for train in trains:
        available_seats = Seat.objects.filter(train=train, is_available=True).count()
        response.append({
            "train_id": train.id,
            "name": train.name,
            "available_seats": available_seats
        })
    return Response(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_seat(request):
    user = request.user
    train_id = request.data['train_id']
    try:
        with transaction.atomic():
            seat = Seat.objects.select_for_update(skip_locked=True).filter(
                train_id=train_id, is_available=True
            ).first()
            if not seat:
                return Response({"error": "No seats available"}, status=HTTP_400_BAD_REQUEST)
            seat.is_available = False
            seat.save()
            booking = Booking.objects.create(user=user, train_id=train_id, seat=seat)
            return Response({"message": "Seat booked", "booking_id": booking.id})
    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking(request, booking_id):
    booking = Booking.objects.filter(id=booking_id, user=request.user).first()
    if not booking:
        return Response({"error": "Booking not found"}, status=HTTP_404_NOT_FOUND)
    return Response({
        "train": booking.train.name,
        "seat": booking.seat.seat_number,
        "booking_time": booking.booking_time
    })
