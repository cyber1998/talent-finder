from django.core.management import BaseCommand
import uuid
from talent.models import Talent


class Command(BaseCommand):
    help = 'Generate base talent'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=str, help='Number of talents to create')

    def handle(self, *args, **options):
        # Create talent
        try:
            quantity = int(options['quantity'])
            talents = [
                Talent(
                    first_name=f'First Name {i}',
                    last_name=f'Last Name {i}', email=f'test_{i}@example.com', reference_id=uuid.uuid4()
                ) for i in
                range(quantity)
            ]
            Talent.objects.bulk_create(talents)
            self.stdout.write(self.style.SUCCESS(f'{quantity} talents created successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating talents: {e}'))


