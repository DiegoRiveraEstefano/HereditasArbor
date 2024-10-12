from django.contrib import admin

from .models import Disease
from .models import DiseaseCategory
from .models import DiseasesParams

admin.site.register(Disease)
admin.site.register(DiseaseCategory)
admin.site.register(DiseasesParams)
