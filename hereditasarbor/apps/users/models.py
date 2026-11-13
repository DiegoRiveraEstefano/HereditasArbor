from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for HereditasArbor.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @cached_property
    def has_personal_data(self) -> bool:
        """Check if user has personal data.

        Returns:
            bool: True if user has personal data, False otherwise.
        """
        return bool(hasattr(self, "personal_data"))

    def get_personal_data(self):
        """Get user's personal data.

        Returns:
            PersonalData: User's personal data.
        """
        return self.personal_data

    def get_tree(self):
        """Get user's family tree.

        Returns:
            FamilyTree: returns the user's family tree
        """
        return self.family_tree
