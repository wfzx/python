# Generated by Django 2.0 on 2020-06-06 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0014_envinfo_tendir'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='OldPort',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
