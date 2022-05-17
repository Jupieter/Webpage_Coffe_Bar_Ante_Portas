# Generated by Django 4.0.4 on 2022-05-17 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('raw_material', '0009_rename_acquisitor_user_productacquisition_acquisiton_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productacquisition',
            name='acquisition_date',
            field=models.DateTimeField(default=0, verbose_name='Beszerzés dátuma'),
        ),
        migrations.AlterField(
            model_name='productacquisition',
            name='store_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Bevételezte', to=settings.AUTH_USER_MODEL, verbose_name='Bevételezte'),
        ),
    ]
