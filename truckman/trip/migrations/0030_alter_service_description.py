# Generated by Django 4.2.4 on 2023-08-28 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0029_service_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
