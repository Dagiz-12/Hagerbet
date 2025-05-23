# Generated by Django 5.2.1 on 2025-05-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loyalty_points', models.PositiveIntegerField(default=0)),
                ('preferred_shipping_address', models.TextField(blank=True, null=True)),
                ('newsletter_subscription', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Customer Profile',
                'verbose_name_plural': 'Customer Profiles',
                'ordering': ['-created_at'],
            },
        ),
    ]
