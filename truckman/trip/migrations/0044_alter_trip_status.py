# Generated by Django 4.2.4 on 2023-08-31 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0043_alter_trip_distance_alter_trip_drop_off_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.CharField(choices=[('NOT STARTED ', 'Not Started'), ('DISPATCHED', 'Dispatched'), ('COMPLETED', 'Completed')], default='Not Started', max_length=30),
        ),
    ]
