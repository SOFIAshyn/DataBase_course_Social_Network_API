# Generated by Django 3.0.6 on 2020-06-06 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_username', models.CharField(max_length=100, null=True)),
                ('fb_password', models.CharField(max_length=100, null=True)),
                ('inst_username', models.CharField(max_length=100, null=True)),
                ('inst_password', models.CharField(max_length=100, null=True)),
                ('tg_username', models.CharField(max_length=100, null=True)),
                ('tg_password', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]