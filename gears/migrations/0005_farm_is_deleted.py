# Generated by Django 2.0.3 on 2018-03-10 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gears', '0004_auto_20180308_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
