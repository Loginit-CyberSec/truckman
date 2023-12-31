# Generated by Django 4.2.4 on 2023-08-16 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_customuser_company'),
        ('trip', '0003_rename_milage_in_vehicle_milage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.client'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle_make',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.client'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle_model',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.client'),
            preserve_default=False,
        ),
    ]
