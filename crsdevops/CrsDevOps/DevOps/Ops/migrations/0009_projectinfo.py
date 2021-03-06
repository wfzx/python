# Generated by Django 2.0 on 2020-05-25 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ops', '0008_modifyserverlog_envpar'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Project', models.CharField(max_length=32)),
                ('EnvPar', models.CharField(max_length=8, null=True)),
                ('Node', models.CharField(max_length=128)),
                ('Port', models.CharField(max_length=6)),
                ('MemSize', models.CharField(max_length=6)),
                ('CheckOpsApi', models.CharField(max_length=128, null=True)),
                ('ServerType', models.CharField(max_length=6, null=True)),
                ('ReSet', models.CharField(max_length=4, null=True)),
                ('Del', models.CharField(max_length=2)),
                ('ModifyTime', models.CharField(max_length=20, null=True)),
                ('CreateTime', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
