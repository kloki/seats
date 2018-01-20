from rest_framework import viewsets

from .models import Event, Guest, BlockedSeat
from .serializers import (EventSerializer, BlockedSeatSerializer,
                          GuestSerializer)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class GuestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class BlockedSeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlockedSeat.objects.all()
    serializer_class = BlockedSeatSerializer
