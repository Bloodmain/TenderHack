from django.contrib import admin
from .models import *


class AdminCompanies(admin.ModelAdmin):
    class Meta:
        model = Companies


admin.site.register(Companies, AdminCompanies)
