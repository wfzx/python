# Generated by Django 2.0 on 2020-07-10 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0041_auto_20200710_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='envinfo',
            name='SkywalkingAddress',
            field=models.TextField(default=0, max_length=1024),
            preserve_default=False,
        ),
    ]
