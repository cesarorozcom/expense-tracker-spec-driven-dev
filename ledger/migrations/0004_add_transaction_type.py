from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0003_recurring_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('payment', 'Payment')], default='payment', max_length=10),
        ),
    ]
