from django.contrib import admin

from hereditasarbor.apps.analytics.models import Analytic
from hereditasarbor.apps.analytics.models import AnalyticPersonal
from hereditasarbor.apps.analytics.models import AnalyticTree

admin.site.register(Analytic)
admin.site.register(AnalyticTree)
admin.site.register(AnalyticPersonal)
