# Generated by Django 4.2.4 on 2023-08-31 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0039_remove_invoice_date_added_remove_invoice_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='status',
            field=models.CharField(choices=[('NOT STARTED ', 'Not Started'), ('DISPATCHED', 'Dispatched'), ('COMPLETED', 'Completed')], default='Not Started'),
        ),
    ]