# Generated by Django 4.2.16 on 2024-11-22 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_systemreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemreport',
            name='purchases_last_hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='systemreport',
            name='returns_last_hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='systemreport',
            name='users_last_hour',
            field=models.IntegerField(default=0),
        ),
    ]