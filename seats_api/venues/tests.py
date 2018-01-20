from django.test import TestCase

from .models import Seat, Section, Venue


def generate_test_venue():
    venue = Venue.objects.create(name="stage1")
    left = Section.objects.create(name="left", rows=5, columns=5, venue=venue)
    right = Section.objects.create(name="right", rows=4, columns=3,
                                   venue=venue)
    for x in range(4):
        for y in range(3):
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
        self.assertEqual(len(layout[self.section1.name]), 5)
        self.assertEqual(len(layout[self.section2.name]), 4)
        self.assertEqual(len(layout[self.section1.name][0]), 5)
        self.assertEqual(len(layout[self.section2.name][0]), 3)
        self.assertEqual(layout[self.section1.name][1][1], "S")
        self.assertEqual(layout[self.section1.name][4][4], "_")

    def test_weird_layout(self):
        Section.objects.create(name="1", rows=1, columns=1, venue=self.venue)
        Section.objects.create(name="0", rows=0, columns=0, venue=self.venue)
        layout = self.venue.layout
        self.assertEqual(len(layout["1"]), 1)
        self.assertEqual(len(layout["0"]), 0)