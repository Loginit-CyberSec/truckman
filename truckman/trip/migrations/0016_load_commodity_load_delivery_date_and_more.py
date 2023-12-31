# Generated by Django 4.2.4 on 2023-08-18 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0015_load_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='commodity',
            field=models.CharField(default='Maize', max_length=155),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='load',
            name='delivery_date',
            field=models.DateField(default='2023-10-10'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='load',
            name='driver_instructions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='load',
            name='quantity',
            field=models.CharField(choices=[('BARREL', 'Barrel'), ('BOXES', 'Boxes'), ('BUSHELS', 'Bushels'), ('CASES', 'Cases'), ('CRATES', 'Crates'), ('GALLONS', 'Gallons'), ('PALLETS', 'Pallets'), ('PIECES', 'Pieces')], default='Barrel', max_length=20),
        ),
        migrations.AddField(
            model_name='load',
            name='quantity_type',
            field=models.CharField(choices=[('BARREL', 'Barrel'), ('BOXES', 'Boxes'), ('BUSHELS', 'Bushels'), ('CASES', 'Cases'), ('CRATES', 'Crates'), ('GALLONS', 'Gallons'), ('PALLETS', 'Pallets'), ('PIECES', 'Pieces')], default='Barrel', max_length=20),
        ),
        migrations.AlterField(
            model_name='load',
            name='fsc_amount_type',
            field=models.CharField(choices=[('FLAT FEE', 'Flat Fee'), ('PER MILE', 'Per Mile'), ('PERCENTAGE', 'Percent')], default='Flat Fee', max_length=30),
        ),
        migrations.AlterField(
            model_name='load',
            name='primary_fee_type',
            field=models.CharField(choices=[('FLAT FEE', 'Flat Fee'), ('PER MILE', 'Per Mile'), ('PER HUNDRED WEIGHT', 'Per Hundred Weight'), ('PER TON', 'Per Ton'), ('PER QUANTITY', 'Per Quantity')], default='Per Mile', max_length=30),
        ),
    ]
