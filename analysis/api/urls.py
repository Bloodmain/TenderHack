from django.urls import path

from .views import *


urlpatterns = [
    path('charts/<str:inn>', ChartsApi.as_view(), name='charts'),
    path('categories/', Categories.as_view(), name='categories'),
]
