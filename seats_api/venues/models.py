from django.db import models
from django.utils.translation import ugettext_lazy as _

from .exceptions import PlaceUnavailableError


class Venue(models.Model):

    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):

    PlaceUnavailableError = PlaceUnavailableError

    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64, unique=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,
                              related_name="sections")

    rows = models.PositiveIntegerField(('number of rows'))
    columns = models.PositiveIntegerField(('number of columns'))

    def place_available(self, row, column):

        if (row > self.rows or column > self.columns or
                bool(self.seats.filter(row=row, column=column))):
            return False
        return True

    def __str__(self):
        return '{}: {}'.format(self.venue.name, self.name)


class Seat(models.Model):
    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                related_name="seats")

    row = models.PositiveIntegerField(('row location'))
    column = models.PositiveIntegerField(('colunm location'))

    def save(self, *args, **kwargs):
        if not self.section.place_available(self.row, self.column):
            raise self.section.PlaceUnavailableError
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} {}-{}'.format(self.section.name, self.row, self.column)
