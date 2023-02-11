# Generated by Django 4.1.5 on 2023-02-06 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0002_alter_categorycommercial_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('short_description', models.CharField(blank=True, max_length=255, verbose_name='short description')),
                ('specifications', models.JSONField(verbose_name='the product specifications')),
                ('categories', models.ManyToManyField(related_name='products', to='catalog.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='tag')),
                ('products', models.ManyToManyField(related_name='tags', to='product.product', verbose_name='products')),
            ],
            options={
                'verbose_name': 'product tag',
                'verbose_name_plural': 'product tags',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products', verbose_name='image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product', verbose_name='product_image')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCommercial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(db_index=True, max_length=512, unique=True, verbose_name='vendor code')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('count', models.IntegerField(verbose_name='left in stock')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Show if product is active and available to search.', verbose_name='is active')),
                ('highlights', models.ManyToManyField(blank=True, related_name='products', to='catalog.categorycommercial')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='commercial', to='product.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product commercial info',
                'verbose_name_plural': 'Products commercial info',
                'ordering': ['price'],
                'abstract': False,
            },
        ),
    ]
