# Generated by Django 4.2.4 on 2023-08-31 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0037_rename_invoice_advance_load_quote_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='load',
            name='customer',
        ),
    ]
