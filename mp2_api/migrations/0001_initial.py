# Generated by Django 2.2.10 on 2020-05-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.IntegerField()),
                ('login_time', models.DateTimeField(auto_now=True)),
                ('logout_time', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
            ],
            options={
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('drone_id', models.AutoField(primary_key=True, serialize=False)),
                ('registered_date', models.DateField(auto_now_add=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('log', models.DecimalField(decimal_places=6, max_digits=9)),
                ('battery_level', models.IntegerField()),
                ('last_accessed', models.DateTimeField(auto_now=True)),
                ('users_connected', models.IntegerField()),
                ('status', models.IntegerField()),
                ('warning_bit', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Drones',
            },
        ),
    ]
