# Generated by Django 4.2.4 on 2023-09-04 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_client_invoice_payment_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='dark_mode',
            field=models.BooleanField(default=False),
        ),
    ]
