# Generated by Django 2.0 on 2020-07-10 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0040_envinfo_javastartpar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addenvlog',
            name='Hosts',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='envinfo',
            name='Hosts',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='envinfo',
            name='JavaStartPar',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='modifyenvlog',
            name='Hosts',
            field=models.TextField(max_length=1024),
        ),
    ]