# Generated by Django 5.0.3 on 2024-10-27 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbook',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]