"""Module for all Form Tests."""

from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.forms import UserCreationForm
from hereditasarbor.apps.users.models import User


class TestUserCreationForm:
    """Test class for all tests related to the UserCreationForm."""

    def test_username_validation_error_msg(self, user: User):
        """Tests UserCreationForm unique validator functions correctly."""
        form = UserCreationForm(
            {
                "username": user.username,
                "email": user.email,
                "password": user.password,
            },
        )

        assert not form.is_valid()
        assert "username" in form.errors
        assert form.errors["username"][0] == _("A user with that username already exists.")
