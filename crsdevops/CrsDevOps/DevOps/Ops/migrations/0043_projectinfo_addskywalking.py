# Generated by Django 2.0 on 2020-07-31 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0042_envinfo_skywalkingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='AddSkywalking',
            field=models.CharField(default=0, max_length=2),
            preserve_default=False,
        ),
    ]
