# Generated by Django 5.0.1 on 2024-03-29 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tyresapp', '0006_remove_tyre_preview_alter_tyreimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tyre',
            name='tread_remain',
            field=models.CharField(max_length=100),
        ),
    ]
