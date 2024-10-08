# Generated by Django 5.1 on 2024-08-22 10:52

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=221)),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Filiallar',
                'db_table': 'branch',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=221, null=True)),
                ('username', models.CharField(blank=True, max_length=221, null=True)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('telegram_id', models.BigIntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Foydalanuvchilar',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Sellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(blank=True, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=221, null=True)),
                ('last_name', models.CharField(blank=True, max_length=221, null=True)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.branch')),
            ],
            options={
                'verbose_name': 'Seller',
                'verbose_name_plural': 'Sotuvchilar',
                'db_table': 'seller',
            },
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.sellers')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.user')),
            ],
            options={
                'verbose_name': 'Mark',
                'verbose_name_plural': 'Baho/Izoh',
                'db_table': 'mark',
            },
        ),
    ]
