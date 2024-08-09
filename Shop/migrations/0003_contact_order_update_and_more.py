# Generated by Django 5.0.7 on 2024-07-21 10:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_selleradditional_verification_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('c_name', models.CharField(default='', max_length=70)),
                ('c_email', models.CharField(default='', max_length=75)),
                ('c_phone', models.CharField(default='', max_length=50)),
                ('c_subject', models.CharField(default='', max_length=100)),
                ('c_message', models.CharField(default='', max_length=1500)),
            ],
        ),
        migrations.CreateModel(
            name='order_update',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('order_desc', models.CharField(max_length=1000)),
                ('order_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='selleradditional',
            name='Verification_Image',
            field=models.ImageField(default=None, upload_to='ArtImages/Seller_Verification'),
        ),
        migrations.AlterField(
            model_name='selleradditional',
            name='store_Logo',
            field=models.ImageField(default=None, upload_to='ArtImages/storesLogo'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.art')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('Order_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_json', models.CharField(max_length=10000)),
                ('Address', models.CharField(max_length=100)),
                ('Zip_Code', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
