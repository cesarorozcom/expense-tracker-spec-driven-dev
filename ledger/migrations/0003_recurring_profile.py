from django.db import migrations, models
import uuid
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_transaction_photo_metadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringProfile',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('frequency', models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])),
                ('interval', models.PositiveIntegerField(default=1, help_text='Repeat every N frequency units')),
                ('next_occurrence', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurrences', to='ledger.account')),
            ],
            options={'ordering': ['-next_occurrence']},
        ),
    ]
