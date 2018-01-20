from django.db import models
from django.utils.translation import ugettext_lazy as _

from .exceptions import PlaceUnavailableError


class Venue(models.Model):

    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64, unique=True)

    @property
    def layout(self):
        return {section.name: section.layout for section in self.sections.all()}

    def __str__(self):
        return self.name


class Section(models.Model):

    PlaceUnavailableError = PlaceUnavailableError

    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,
                              related_name="sections")

    rows = models.PositiveIntegerField(('number of rows'))
    columns = models.PositiveIntegerField(('number of columns'))

    def place_available(self, row, column):

        if (row > self.rows or column > self.columns or
                bool(self.seats.filter(row=row, column=column))):
            return False
        return True

    def generate_seats(self):
        for row in range(self.rows):
            for column in range(self.columns):
                Seat.objects.create(name='{}{}'.format(row, column),
                                    section=self, row=row, column=column)

    @property
    def layout(self):
        """ The layout of a sections is represented as a list for each row
        A row is represented as a list, "_" means no seat, "S" means seats
        """
        matrix = [list("_" * self.columns) for _ in range(self.rows)]
        for seat in self.seats.all():
            matrix[seat.row][seat.column] = "S"
        return matrix

    def __str__(self):
        return '{}: {}'.format(self.venue.name, self.name)


class Seat(models.Model):
    added = models.DateTimeField(_('added'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    name = models.CharField(_('name'), max_length=64)
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
