from django.contrib import admin
from .models import Appointment, CustomUser

admin.site.register(Appointment)
admin.site.register(CustomUser)
