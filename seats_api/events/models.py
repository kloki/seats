from django.db import models
from django.utils.translation import ugettext_lazy as _

from venues.models import Venue, Seat

from .exceptions import SeatUnavailableError


class Event(models.Model):

    SeatUnavailableError = SeatUnavailableError

    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64, unique=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,
                              related_name="events")

    def seat_available(self, seat):
        if bool(self.guests.filter(seat=seat)):
            return False
        return True

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
