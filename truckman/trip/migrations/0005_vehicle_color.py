# Generated by Django 4.2.4 on 2023-08-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_vehicle_company_vehicle_make_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='color',
            field=models.CharField(blank=True, null=True),
        ),
    ]
