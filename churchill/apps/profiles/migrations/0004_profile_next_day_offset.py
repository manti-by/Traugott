# Generated by Django 3.1.8 on 2021-04-28 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210316_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='next_day_offset',
            field=models.IntegerField(blank=True, default=8, help_text='Offset in hours for the next day'),
        ),
    ]
