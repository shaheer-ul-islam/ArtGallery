# Generated by Django 5.0.7 on 2024-07-21 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0003_contact_order_update_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_Method',
            field=models.BooleanField(default=False),
        ),
    ]
