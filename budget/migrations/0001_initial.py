# Generated by Django 5.1.2 on 2024-10-13 13:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(verbose_name='Дата завершения')),
                ('budget', models.JSONField(default=dict, verbose_name='Бюджет')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Бюджет',
                'verbose_name_plural': 'Бюджеты',
                'db_table': 'budgets',
            },
        ),
    ]
