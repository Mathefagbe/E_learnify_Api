# Generated by Django 4.1 on 2023-08-07 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_transactionlog_order_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionlog',
            old_name='order_id',
            new_name='course_id',
        ),
    ]