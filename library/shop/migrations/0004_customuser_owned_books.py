# Generated by Django 5.1.2 on 2024-10-28 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_book_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='owned_books',
            field=models.ManyToManyField(blank=True, related_name='owners', to='shop.book'),
        ),
    ]
