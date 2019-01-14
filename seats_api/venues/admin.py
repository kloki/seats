from django.contrib import admin

from .models import Venue, Section, Seat

admin.site.register(Venue)
admin.site.register(Section)
admin.site.register(Seat)