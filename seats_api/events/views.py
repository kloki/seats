from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from venues.models import Section
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


class AddGroupView(APIView):
    """ Add a group. Fields:
            {"event": pk
             "section": pk(optional),
             "guest":list of strings}
    """
    def post(self, request, format=None):
        valid, event, guests, section = self.validate_data(request.data)
        if not valid:
            return Response(
                {
                    "success": False,
                    "message": "invalid/missing parameters"
                }, status=HTTP_400_BAD_REQUEST)

        try:
            event.add_group(guests, section_preference=section)
        except Event.NoRoomError:
            return Response(
                {
                    "success": False,
                    "message": "No room for group"

                }, status=HTTP_400_BAD_REQUEST)

        return Response({"success": True})

    def validate_data(self, data):
        """TODO use serializer, ran out of time
        """
        try:
            event_id = data["event"]
            guests = data["guests"]
            section = data.get("section", None)
        except KeyError:
            return False, "", "", ""
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return False, "", "", ""
        if not isinstance(guests, list):
            return False, "", "", ""
        if section is not None:
            try:
                event.venue.sections.get(pk=section)
            except Section.DoesNotExist:
                return False, "", "", ""
        return True, event, guests, section
