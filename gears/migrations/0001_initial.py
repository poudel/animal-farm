# Generated by Django 2.0 on 2017-12-30 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('tag', models.CharField(max_length=100)),
                ('dob_bs', models.CharField(blank=True, max_length=15, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalTxn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('amount', models.BigIntegerField()),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gears.Animal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnimalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('breeding_ages', models.CharField(blank=True, max_length=200)),
                ('animal_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gears.AnimalType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TxnType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('name_np', models.CharField(blank=True, max_length=200)),
                ('is_expense', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='txntype',
            unique_together={('name', 'is_expense')},
        ),
        migrations.AddField(
            model_name='animaltxn',
            name='txn_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gears.TxnType'),
        ),
        migrations.AddField(
            model_name='animal',
            name='breed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gears.Breed'),
        ),
        migrations.AddField(
            model_name='animal',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gears.Farm'),
        ),
        migrations.AlterUniqueTogether(
            name='animal',
            unique_together={('farm', 'tag')},
        ),
    ]
