# Generated by Django 2.0 on 2020-07-10 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0039_auto_20200710_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='envinfo',
            name='JavaStartPar',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]