from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("analysis.urls")),
    path('api/', include("analysis.api.urls"))
]
