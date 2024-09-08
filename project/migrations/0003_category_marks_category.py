# Generated by Django 5.1 on 2024-08-26 04:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_marks_options_alter_sellers_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=221)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Baholash kategoriyalari',
                'db_table': 'category',
            },
        ),
        migrations.AddField(
            model_name='marks',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.category'),
            preserve_default=False,
        ),
    ]