# Generated by Django 4.1.5 on 2023-01-15 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_rename_characters_product_specifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcommercial',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='commercial', to='product.product', verbose_name='Product'),
        ),
    ]