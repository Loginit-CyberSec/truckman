# Generated by Django 4.2.4 on 2023-08-28 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0031_payment_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='is_assigned_driver',
            field=models.BooleanField(default=False),
        ),
    ]
