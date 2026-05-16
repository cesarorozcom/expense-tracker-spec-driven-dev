"""Initial migration for ledger app."""
from django.db import migrations, models
import uuid
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('occurred_at', models.DateTimeField()),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('photo', models.ImageField(upload_to='receipts/', null=True, blank=True)),
                ('is_recurring', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='ledger.Account')),
            ],
            options={'ordering': ['-occurred_at']},
        ),
    ]
