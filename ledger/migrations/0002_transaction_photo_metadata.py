"""Add photo metadata fields to transaction model."""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='photo_status',
            field=models.CharField(
                choices=[('unverified', 'Unverified'), ('verified', 'Verified'), ('failed', 'Failed')],
                default='unverified',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='transaction',
            name='photo_uploaded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
