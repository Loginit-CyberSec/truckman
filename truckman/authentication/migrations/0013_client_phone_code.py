# Generated by Django 4.2.4 on 2023-09-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone_code',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
