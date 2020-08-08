# Generated by Django 2.0 on 2020-07-07 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Address', models.CharField(max_length=256)),
                ('RequestMethod', models.CharField(max_length=8)),
                ('RequestHeader', models.CharField(max_length=200)),
                ('Template', models.CharField(max_length=400)),
            ],
        ),
    ]
