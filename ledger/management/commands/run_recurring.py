from django.core.management.base import BaseCommand
from django.utils import timezone
from ledger.models import RecurringProfile, Transaction

class Command(BaseCommand):
    help = 'Generate transactions for due recurring profiles.'

    def handle(self, *args, **options):
        now = timezone.now()
        due = RecurringProfile.objects.filter(active=True, next_occurrence__lte=now)
        created = 0
        for profile in due:
            try:
                # create transaction
                tx = Transaction.objects.create(
                    account=profile.account,
                    occurred_at=profile.next_occurrence,
                    amount=profile.amount,
                    description=profile.description or f"Recurring: {profile.frequency}",
                    is_recurring=True,
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created transaction {tx.id} for profile {profile.id}'))

                # advance next_occurrence until it's in the future
                while profile.is_due(at=timezone.now()):
                    profile.advance_next()
            except Exception as e:
                self.stderr.write(f'Failed to create transaction for profile {profile.id}: {e}')
        self.stdout.write(self.style.SUCCESS(f'Generated {created} transactions.'))
