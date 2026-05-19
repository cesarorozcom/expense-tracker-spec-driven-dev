from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the first application user (idempotent by username)."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="Username for the first user")
        parser.add_argument("--email", required=True, help="Email for the first user")
        parser.add_argument("--password", required=True, help="Password for the first user")
        parser.add_argument(
            "--superuser",
            action="store_true",
            help="Create as superuser/staff",
        )

    def handle(self, *args, **options):
        username = options["username"].strip()
        email = options["email"].strip()
        password = options["password"]
        make_superuser = options["superuser"]

        if not username:
            raise CommandError("--username cannot be empty")
        if not email:
            raise CommandError("--email cannot be empty")
        if not password:
            raise CommandError("--password cannot be empty")

        user_model = get_user_model()

        if user_model.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists. No changes made."))
            return

        if make_superuser:
            user = user_model.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
        else:
            user = user_model.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

        role = "superuser" if make_superuser else "user"
        self.stdout.write(self.style.SUCCESS(f"Created {role} '{user.username}' successfully."))
