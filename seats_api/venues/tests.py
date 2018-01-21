from django.test import TestCase

from .models import Seat, Section, Venue


def generate_test_venue():
    venue = Venue.objects.create(name="stage1")
    left = Section.objects.create(name="left", rows=5, columns=5, venue=venue)
    right = Section.objects.create(name="right", rows=4, columns=3,
                                   venue=venue)
    left.generate_seats()
    right.generate_seats()
    # One seat is missing
    Seat.objects.get_seat_by_location(left.pk, 4, 4).delete()
    return venue, left, right


class TestInvalidSeats(TestCase):

    def setUp(self):
        self.venue, self.section1, self.section2 = generate_test_venue()

    def test_correct(self):
        seat = Seat(name='test', section=self.section1, row=5, column=4)
        seat.save()

    def test_place_doesnt_exist(self):
        with self.assertRaises(Section.PlaceUnavailableError):
            seat = Seat(name='test', section=self.section2, row=4, column=4)
            seat.save()

    def test_place_taken(self):
        with self.assertRaises(Section.PlaceUnavailableError):
            seat = Seat(name='test', section=self.section2, row=1, column=1)
            seat.save()


class TestSeatGenerator(TestCase):

    def test(self):
        venue = Venue.objects.create(name="stage1")
        test = Section.objects.create(name="test", rows=5,
                                      columns=5, venue=venue)
        test.generate_seats()
        self.assertEqual(len(Seat.objects.all()), 25)


class TestLayouts(TestCase):

    def setUp(self):
        self.venue, self.section1, self.section2 = generate_test_venue()

    def test_correct(self):
        layout = self.venue.layout
        self.assertEqual(len(layout.keys()), 2)
        self.assertEqual(len(layout[self.section1.pk]), 5)
        self.assertEqual(len(layout[self.section2.pk]), 4)
        self.assertEqual(len(layout[self.section1.pk][0]), 5)
        self.assertEqual(len(layout[self.section2.pk][0]), 3)
        self.assertEqual(layout[self.section1.pk][1][1], "S")
        self.assertEqual(layout[self.section1.pk][4][4], "_")

    def test_weird_layout(self):
        s1 = Section.objects.create(name="1", rows=1, columns=1,
                                    venue=self.venue)
        s2 = Section.objects.create(name="0", rows=0, columns=0,
                                    venue=self.venue)
        layout = self.venue.layout
        self.assertEqual(len(layout[s1.pk]), 1)
        self.assertEqual(len(layout[s2.pk]), 0)
