# Generated by Django 5.1.2 on 2024-10-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_transactions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_transaction',
            field=models.DateTimeField(verbose_name='Дата транзакции'),
        ),
    ]
