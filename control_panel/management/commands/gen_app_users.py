from django.core.management import BaseCommand

from control_panel.models import AppUser


class Command(BaseCommand):
    help = 'Generate app users'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('password', type=str, help='Password of the user')
        parser.add_argument('email', type=str, help='Email of the user')

    def handle(self, *args, **options):
        # Create superuser
        if not AppUser.objects.filter(username=options['username']).exists():
            AppUser.objects.create_superuser(username=options['username'], password=options['password'], email=options['email'])
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.ERROR('Superuser already exists'))


