# Generated by Django 5.1.2 on 2024-10-12 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_transactions', '0003_alter_transaction_date_transaction'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, verbose_name='Celery id')),
                ('report', models.CharField(blank=True, max_length=255, null=True, verbose_name='Путь к отчету')),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('error', 'Error')], default='in_progress', max_length=20, verbose_name='Статус отчета')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='Ошибка')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_result', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
