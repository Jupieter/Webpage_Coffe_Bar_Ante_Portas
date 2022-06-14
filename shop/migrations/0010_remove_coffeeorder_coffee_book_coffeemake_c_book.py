# Generated by Django 4.0.4 on 2022-06-13 13:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_coffeeorder_coffee_book_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffeeorder',
            name='coffee_book',
        ),
        migrations.AddField(
            model_name='coffeemake',
            name='c_book',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Könyvelés dátuma'),
        ),
    ]