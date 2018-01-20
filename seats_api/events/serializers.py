from rest_framework import serializers

from .models import Event, Guest, BlockedSeat


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'venue', 'added', 'updated',
                  'layout', 'guests')


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'name', 'group', 'seat',
                  'event', 'added', 'updated')


class BlockedSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedSeat
        fields = ('id', 'reason', 'seat', 'event', 'added', 'updated')
