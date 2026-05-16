from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from ledger.models import Transaction
import os

class Command(BaseCommand):
    help = 'Purge transaction photo files older than PHOTO_RETENTION_DAYS and mark photo fields null.'

    def handle(self, *args, **options):
        retention = getattr(settings, 'PHOTO_RETENTION_DAYS', 365)
        cutoff = timezone.now() - timezone.timedelta(days=int(retention))
        qs = Transaction.objects.filter(photo__isnull=False, photo_uploaded_at__lt=cutoff)
        total = qs.count()
        removed = 0
        for tx in qs:
            try:
                # delete file from storage
                if tx.photo and os.path.exists(tx.photo.path):
                    os.remove(tx.photo.path)
                tx.photo = None
                tx.photo_status = 'failed'
                tx.save(update_fields=['photo', 'photo_status'])
                removed += 1
            except Exception as e:
                self.stderr.write(f'Failed to purge photo for transaction {tx.id}: {e}')
        self.stdout.write(self.style.SUCCESS(f'Purged {removed}/{total} photos older than {retention} days.'))
