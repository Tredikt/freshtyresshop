# Generated by Django 5.0.1 on 2024-05-01 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tyresapp', '0009_filtration_sorting_tyre_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Filtration',
        ),
        migrations.DeleteModel(
            name='Sorting',
        ),
    ]
