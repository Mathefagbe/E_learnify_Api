# Generated by Django 4.1 on 2023-07-31 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('my_subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mylearning',
            name='course',
            field=models.ManyToManyField(blank=True, related_name='mylearning', to='courses.course'),
        ),
    ]
