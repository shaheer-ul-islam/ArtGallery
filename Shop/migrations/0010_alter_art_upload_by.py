# Generated by Django 5.0.6 on 2024-07-23 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0009_alter_art_upload_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='art',
            name='upload_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Shop.seller'),
        ),
    ]
