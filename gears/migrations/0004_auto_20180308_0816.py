# Generated by Django 2.0.3 on 2018-03-08 02:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gears', '0003_auto_20180308_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='has_dairy_cattle',
            field=models.BooleanField(default=True, verbose_name='has dairy cattle'),
        ),
        migrations.AlterField(
            model_name='farm',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='farms', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
