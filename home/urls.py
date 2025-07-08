from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('private/events', PrivateEventViewset, basename='private-event')
router.register('public/events', PublicEventViewset, basename='public-event')

urlpatterns = [
        path('register/', RegisterAPI.as_view(), name='register'),
        path('login/', LoginAPI.as_view(), name='login'),
        path('', include(router.urls)),
       
]
