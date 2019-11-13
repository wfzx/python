# Generated by Django 2.2.7 on 2019-11-13 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_user_invicode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('invitacode', models.CharField(max_length=6)),
                ('invitaname', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='invicode',
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(max_length=32),
        ),
    ]