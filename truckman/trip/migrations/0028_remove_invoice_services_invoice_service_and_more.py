# Generated by Django 4.2.4 on 2023-08-28 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0027_invoice_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='services',
        ),
        migrations.AddField(
            model_name='invoice',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trip.service'),
        ),
        migrations.AddField(
            model_name='trip',
            name='distance',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='drop_off_location',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='pick_up_location',
            field=models.CharField(null=True),
        ),
    ]
