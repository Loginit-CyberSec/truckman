# Generated by Django 4.2.4 on 2023-08-17 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_customuser_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
