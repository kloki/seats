from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from events.views import (EventViewSet, GuestViewSet, BlockedSeatViewSet,
                          AddGroupView)
from venues.views import VenueViewSet, SectionViewSet, SeatViewSet

api_router = DefaultRouter()
api_router.register(r'venues', VenueViewSet)
api_router.register(r'section', SectionViewSet)
api_router.register(r'seats', SeatViewSet)
api_router.register(r'events', EventViewSet)
api_router.register(r'guests', GuestViewSet)
api_router.register(r'blockedseats', BlockedSeatViewSet)


schema_view = get_swagger_view(title='Seats API')

urlpatterns = [
    url(r'^api/add-group/', AddGroupView.as_view()),
    url(r'^api/', include(api_router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^schema/', schema_view)
]
