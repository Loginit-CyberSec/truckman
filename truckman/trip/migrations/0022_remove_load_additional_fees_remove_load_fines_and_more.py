# Generated by Django 4.2.4 on 2023-08-23 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0021_driver_id_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='load',
            name='additional_fees',
        ),
        migrations.RemoveField(
            model_name='load',
            name='fines',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='driver',
        ),
        migrations.AddField(
            model_name='load',
            name='broker_commission',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='driver_milage',
            field=models.FloatField(null=True),
        ),
    ]