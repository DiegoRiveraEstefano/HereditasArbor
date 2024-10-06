from django.contrib import admin

from .models import Disease
from .models import DiseaseCategory

admin.site.register((Disease, DiseaseCategory))
