# Generated by Django 4.2.4 on 2023-09-08 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_alter_client_phone_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_code',
            field=models.CharField(default='+254', max_length=12),
        ),
    ]