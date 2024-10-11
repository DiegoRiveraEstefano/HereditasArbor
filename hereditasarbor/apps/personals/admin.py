from django.contrib import admin

from .models import PersonalData
from .models import PersonalTimeStampData

admin.site.register(PersonalData)
admin.site.register(PersonalTimeStampData)
