# Generated by Django 5.2.3 on 2025-07-08 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_booking_booking_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='total_person',
            field=models.IntegerField(default=1),
        ),
    ]
