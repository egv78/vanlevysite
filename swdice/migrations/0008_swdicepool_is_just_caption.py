# Generated by Django 2.0.7 on 2018-11-06 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swdice', '0007_auto_20181106_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='swdicepool',
            name='is_just_caption',
            field=models.BooleanField(default=True),
        ),
    ]
