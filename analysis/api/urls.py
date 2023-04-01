from django.urls import path

from .views import *


urlpatterns = [
    path('charts/', ChartsApi.as_view(), name='charts'),
    path('categories/', Categories.as_view(), name='categories'),
    path('regions/', Regions.as_view(), name='regions'),
]
