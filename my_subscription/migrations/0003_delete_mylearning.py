# Generated by Django 4.1 on 2023-08-01 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_subscription', '0002_alter_mylearning_course'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyLearning',
        ),
    ]