from django.core.management.base import BaseCommand

from hereditasarbor.apps.users.models import User


class Command(BaseCommand):
    help = "Create a admin user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args, **options):
        new_admin = User.objects.create(
            username=options["username"].split("=")[-1],
            email=options["email"].split("=")[-1],
            password=options["password"].split("=")[-1],
        )
        self.stdout.write(
            self.style.SUCCESS('a"{}"'.format(options["username"].split("=")[-1])),
        )
        new_admin.is_active = True
        new_admin.is_staff = True
        new_admin.is_superuser = True
        new_admin.set_password(raw_password=options["password"])
        new_admin.save()
        new_admin.check_password(raw_password=options["password"])
        new_admin.save()
        new_admin.full_clean()
        new_admin.set_password(raw_password=options["password"])
        new_admin.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully user "{new_admin.has_usable_password()}"',
            ),
        )
