# Generated by Django 2.0 on 2020-06-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0023_envconninfo_modifytime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addenvconnlog',
            name='ModifyTime',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='envconninfo',
            name='ModifyTime',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='modifyenvconnlog',
            name='ModifyTime',
            field=models.CharField(max_length=20),
        ),
    ]
