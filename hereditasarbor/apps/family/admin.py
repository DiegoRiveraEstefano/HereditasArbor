from django.contrib import admin

from .models import Familiar
from .models import FamilyTree

admin.site.register((Familiar, FamilyTree))
