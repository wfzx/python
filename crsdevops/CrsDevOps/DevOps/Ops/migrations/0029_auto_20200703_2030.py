# Generated by Django 2.0 on 2020-07-03 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0028_projectinfo_checkapitime'),
    ]

    operations = [
        migrations.CreateModel(
            name='CronExecReco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ExecTime', models.CharField(max_length=64)),
            ],
        ),
        migrations.DeleteModel(
            name='Crontab',
        ),
    ]