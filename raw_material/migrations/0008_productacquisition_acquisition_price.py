# Generated by Django 4.0.4 on 2022-05-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raw_material', '0007_waretypes_ware_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productacquisition',
            name='acquisition_price',
            field=models.IntegerField(default=0, verbose_name='Ára [Ft]'),
        ),
    ]
