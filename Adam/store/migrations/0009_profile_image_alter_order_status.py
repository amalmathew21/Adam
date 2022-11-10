# Generated by Django 4.1.2 on 2022-11-10 13:57

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='images/users.png', upload_to=store.models.Profile.image_upload_to),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Out for Shipping', 'Out for Shipping')], default='Pending', max_length=150),
        ),
    ]