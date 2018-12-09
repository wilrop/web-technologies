# Generated by Django 2.1.2 on 2018-12-09 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0003_remove_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=250)),
                ('postal_code', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
