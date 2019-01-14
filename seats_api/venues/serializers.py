from rest_framework import serializers

from .models import Venue, Section, Seat


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('id', 'name', 'sections', 'added', 'updated', 'layout')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'venue', 'rows', 'layout'
                  'columns', 'added', 'updated')


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id', 'name', 'section', 'row',
                  'column', 'added', 'updated')
