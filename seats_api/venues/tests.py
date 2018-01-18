from django.test import TestCase

from .models import Seat, Section, Venue


def generate_test_venue():
    venue = Venue.objects.create(name="stage1")
    left = Section.objects.create(name="left", rows=5, columns=5, venue=venue)
    right = Section.objects.create(name="right", rows=4, columns=3,
                                   venue=venue)
    for x in range(3):
        for y in range(2):
            Seat.objects.create(name='l{}{}'.format(x, y),
                                section=left, row=x, column=y)
            Seat.objects.create(name='r{}{}'.format(x, y),
                                section=right, row=x, column=y)
    return venue, left, right


class TestInvalidSeats(TestCase):

    def setUp(self):
        self.venue, self.section1, self.section2 = generate_test_venue()

    def test_correct(self):
        seat = Seat(name='test', section=self.section1, row=5, column=4)
        seat.save()

    def test_place_doesnt_exist(self):
        with self.assertRaises(Section.PlaceUnavailableError):
            seat = Seat(name='test', section=self.section2, row=5, column=4)
            seat.save()

    def test_place_taken(self):
        with self.assertRaises(Section.PlaceUnavailableError):
            seat = Seat(name='test', section=self.section2, row=1, column=1)
            seat.save()
