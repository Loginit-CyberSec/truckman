# Generated by Django 4.2.4 on 2023-08-28 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0025_invoice_tax_alter_service_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='valid_till',
        ),
    ]
