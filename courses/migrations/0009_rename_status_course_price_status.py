# Generated by Django 4.1 on 2023-08-05 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_course_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='status',
            new_name='price_status',
        ),
    ]
