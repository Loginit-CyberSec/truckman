# Generated by Django 4.2.4 on 2023-08-17 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0011_rename_id_no_customer_address_one_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='credit_limit',
            field=models.IntegerField(null=True),
        ),
    ]
