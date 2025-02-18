# Generated by Django 5.1.4 on 2025-01-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='summ',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='address',
            name='korp',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='building',
            name='cleaning_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='building',
            name='number_of_chutes',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='number_of_elevators',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='number_of_entrances',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='number_of_floors',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='building',
            name='number_of_residents',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='residential_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
