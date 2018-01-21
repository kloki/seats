from django.test import TestCase

from venues.models import Seat
from venues.tests import generate_test_venue

from .models import Event, Guest, BlockedSeat


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

    def test_blocked_seat(self):
        BlockedSeat.objects.create(event=self.event, seat=Seat.objects.all()[1])

        with self.assertRaises(Event.SeatUnavailableError):
            guest = Guest(name="test2", event=self.event,
                          seat=Seat.objects.all()[1])
            guest.save()


class TestLayouts(TestCase):

    def setUp(self):
        self.event = generate_test_event()
        self.seat1 = Seat.objects.all()[0]
        self.seat2 = Seat.objects.all()[1]
        Guest.objects.create(name="test2", event=self.event,
                             seat=self.seat1)
        BlockedSeat.objects.create(event=self.event, seat=self.seat2)

    def test_correct(self):
        layout = self.event.layout
        self.assertEqual(layout[self.seat1.section.pk][self.seat1.row][self.seat1.column],
                         "G")
        self.assertEqual(layout[self.seat2.section.pk][self.seat2.row][self.seat2.column],
                         "B")


class TestLocationFinding(TestCase):

    def setUp(self):
        self.event = generate_test_event()
        self.sections = [section.pk for section in self.event.venue.sections.all()]

    def test_empty_event(self):
        location = self.event.parse_layout(self.sections, 2)
        self.assertEqual(location[0], 0)
        self.assertEqual(location[1], 0)

    def test_section_event(self):
        location = self.event.parse_layout([self.sections[1]], 2)
        self.assertEqual(location[2], self.sections[1])

    def test_no_room(self):
        with self.assertRaises(Event.NoRoomError):
            self.event.parse_layout([self.sections[1]], 100)

    def test_second_row(self):
        Guest.objects.create(name="test2", event=self.event,
                             seat=Seat.objects.get_seat_by_location(
                                 self.sections[1], 0, 0))
        location = self.event.parse_layout([self.sections[1]], 3)
        self.assertEqual(location[0], 1)

    def test_blocked_seat(self):
        BlockedSeat.objects.create(
            event=self.event, seat=Seat.objects.get_seat_by_location(
                self.sections[0], 0, 1))
        location = self.event.parse_layout([self.sections[0]], 2)
        self.assertEqual(location[0], 0)
        self.assertEqual(location[1], 2)

    def test_blocked_seat_forced_next_row(self):
        BlockedSeat.objects.create(
            event=self.event, seat=Seat.objects.get_seat_by_location(
                self.sections[0], 0, 1))
        location = self.event.parse_layout([self.sections[0]], 5)
        self.assertEqual(location[0], 1)
        self.assertEqual(location[1], 0)


class TestAssignLocation(TestCase):

    def setUp(self):
        self.event = generate_test_event()
        self.sections = [section.pk for section in self.event.venue.sections.all()]

    def test_seats_connected(self):
        seats = self.event.assign_location(self.sections[0], 5)
        self.assertTrue(all(x for x in seats if x.row == 0))
        self.assertTrue(all(x for x in seats if x.section.pk == self.sections[0]))
        self.assertTrue(any(x for x in seats if x.column == 0))
        self.assertTrue(any(x for x in seats if x.column == 1))
        self.assertTrue(any(x for x in seats if x.column == 2))
        self.assertTrue(any(x for x in seats if x.column == 3))
        self.assertTrue(any(x for x in seats if x.column == 4))


class TestGuestCreation(TestCase):

    def setUp(self):
        self.event = generate_test_event()
        self.sections = [section.pk for section in self.event.venue.sections.all()]

    def test(self):
        self.event.add_group(guests=["a", "b", "c"])
        self.assertTrue(len(Guest.objects.all()), 3)
        seats = [guest.seat for guest in Guest.objects.all()]
        self.assertTrue(all(x for x in seats if x.row == 0))
        self.assertTrue(all(x for x in seats if x.section.pk == self.sections[0]))
        self.assertTrue(any(x for x in seats if x.column == 0))
        self.assertTrue(any(x for x in seats if x.column == 1))
        self.assertTrue(any(x for x in seats if x.column == 2))
