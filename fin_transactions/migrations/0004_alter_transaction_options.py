# Generated by Django 5.1.2 on 2024-10-11 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fin_transactions', '0003_alter_transaction_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'verbose_name': 'Транзакция', 'verbose_name_plural': 'Транзакции'},
        ),
    ]
