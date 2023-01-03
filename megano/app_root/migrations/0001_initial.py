# Generated by Django 4.1.2 on 2022-11-22 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery', models.CharField(choices=[('BD', 'Basic delivery'), ('ED', 'Express delivery')], max_length=32, verbose_name='delivery')),
                ('debug_mode', models.BooleanField(default=True, verbose_name='debug mode')),
                ('is_payment_available', models.BooleanField(default=True, help_text='Is payment available on the site at the moment?', verbose_name='payment')),
                ('superuser_only', models.BooleanField(default=False, help_text='Is admin pages available for all staff users?', verbose_name='superuser only')),
            ],
        ),
    ]