# Generated by Django 2.1.2 on 2018-11-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacies', '0004_auto_20181120_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product_stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
