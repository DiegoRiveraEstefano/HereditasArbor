from http import HTTPStatus

import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.forms import UserAdminChangeForm
from hereditasarbor.apps.users.models import User
from hereditasarbor.apps.users.tests.factories import UserFactory
from hereditasarbor.apps.users.views import UserRedirectView
from hereditasarbor.apps.users.views import UserUpdateView
from hereditasarbor.apps.users.views import user_detail_view

pytestmark = pytest.mark.django_db
