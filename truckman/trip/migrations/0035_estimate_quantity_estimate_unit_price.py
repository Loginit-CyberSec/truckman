# Generated by Django 4.2.4 on 2023-08-29 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0034_estimate_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='quantity',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='estimate',
            name='unit_price',
            field=models.IntegerField(default=0.0),
        ),
    ]
