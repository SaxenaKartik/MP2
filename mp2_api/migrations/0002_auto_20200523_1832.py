# Generated by Django 2.2.10 on 2020-05-23 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp2_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='login_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
