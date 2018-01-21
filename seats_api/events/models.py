from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _

from venues.models import Venue, Seat

from .exceptions import SeatUnavailableError, NoRoomError


class Event(models.Model):

    SeatUnavailableError = SeatUnavailableError
    NoRoomError = NoRoomError

    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64, unique=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,
                              related_name="events")

    @property
    def layout(self):
        """ Uses the same layout format as venue, but uses "G" for guests
        and "B" for blocked seats:
        """
        layout = self.venue.layout
        for blocked in self.blocked_seats.all():
            s = blocked.seat
            layout[s.section.pk][s.row][s.column] = "B"

        for guest in self.guests.all():
            s = guest.seat
            layout[s.section.pk][s.row][s.column] = "G"

        return layout

    def seat_available(self, seat):
        if (bool(self.guests.filter(seat=seat)) or
                bool(self.blocked_seats.filter(seat=seat))):
            return False
        return True

    def add_group(self, guests, section_preferences=None):
        """ guests are a list of name. section_preferences is a list
        of section names that are valid sections
        """
        seats = self.assign_location(section_preferences, len(guests))
        group = uuid4()
        for guest in guests:
            Guest.objects.create(name=guest, seat=seats.pop(),
                                 event=self, group=group)

    def assign_location(self, section_preferences, group_size):
        """ This will generate a list of seat locations to be used by a group.
        It will try a section a time, and first row to last row, left to right.
        """
        if section_preferences is None:
            section_preferences = self.layout.keys()
        location = self.parse_layout(section_preferences, group_size)
        seats = []
        for i in range(group_size):
            seats.append(Seat.objects.get_seat_by_location(
                section=location[2],
                row=location[0],
                column=location[1] + i))
        return seats

    def parse_layout(self, sections, group_size):
        """ We concate the row to a string and let str.index to
        searching for us
        """
        layout = self.layout
        for section in sections:
            for row in layout[section]:
                try:
                    column = "".join(row).index("S" * group_size)
                    return (layout[section].index(row), column, section)
                except ValueError:
                    # There is no room in this row
                    pass
        # Could Not find an room for the group in all sections
        raise NoRoomError

    def __str__(self):
        return self.name


class Guest(models.Model):
    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64)
    group = models.CharField(_('group'), max_length=64)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              related_name="guests")

    def save(self, *args, **kwargs):
        if not self.event.seat_available(self.seat):
            raise self.event.SeatUnavailableError
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlockedSeat(models.Model):
    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    reason = models.CharField(_('reason'), max_length=256)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              related_name="blocked_seats")

    def save(self, *args, **kwargs):
        if not self.event.seat_available(self.seat):
            raise self.event.SeatUnavailableError
        super().save(*args, **kwargs)
