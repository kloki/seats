from django.contrib import admin

from .models import Event, Guest, BlockedSeat

admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(BlockedSeat)
