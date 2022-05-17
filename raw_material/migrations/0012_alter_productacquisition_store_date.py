# Generated by Django 4.0.4 on 2022-05-17 12:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('raw_material', '0011_alter_productacquisition_acquisition_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productacquisition',
            name='store_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Raktározás dátuma'),
        ),
    ]
