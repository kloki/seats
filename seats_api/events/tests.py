from django.test import TestCase

from venues.models import Seat
from venues.tests import generate_test_venue

from .models import Event, Guest


def generate_test_event():
    venue, _, _ = generate_test_venue()
    return Event.objects.create(name="test_event", venue=venue)


class TestInvalidGuests(TestCase):

    def setUp(self):
        self.event = generate_test_event()

    def test_correct(self):
        Guest.objects.create(name="test1", event=self.event,
                             seat=Seat.objects.all()[1])
        guest = Guest(name="test2", event=self.event,
                      seat=Seat.objects.all()[0])
        guest.save()

    def test_double_booking_attempt(self):
        Guest.objects.create(name="test1", event=self.event,
                             seat=Seat.objects.all()[1])

        with self.assertRaises(Event.SeatUnavailableError):
            guest = Guest(name="test2", event=self.event,
                          seat=Seat.objects.all()[1])
            guest.save()
