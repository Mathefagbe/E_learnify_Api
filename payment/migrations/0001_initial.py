# Generated by Django 4.1 on 2023-08-07 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPaymentInfo',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_id', models.UUIDField(blank=True, null=True)),
                ('checkout_id', models.BigIntegerField(blank=True, default=0, null=True)),
                ('txRef', models.CharField(blank=True, max_length=20, null=True)),
                ('amount', models.BigIntegerField(blank=True, default=0, null=True)),
                ('currency', models.CharField(blank=True, max_length=5, null=True)),
                ('status', models.CharField(max_length=15, null=True)),
                ('transactionComplete', models.BooleanField(default=False)),
                ('chargedAmount', models.BigIntegerField(default=0)),
                ('customer_code', models.CharField(blank=True, max_length=30, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('paid_date', models.DateTimeField(blank=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('authorization_code', models.CharField(blank=True, max_length=100, null=True)),
                ('card_type', models.CharField(blank=True, max_length=10, null=True)),
                ('last4', models.CharField(blank=True, max_length=4, null=True)),
                ('exp_month', models.CharField(blank=True, max_length=10, null=True)),
                ('exp_year', models.CharField(blank=True, max_length=10, null=True)),
                ('bin', models.CharField(blank=True, max_length=10, null=True)),
                ('bank', models.CharField(blank=True, max_length=100, null=True)),
                ('account_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userpayment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('order_id', models.UUIDField(blank=True, null=True, unique=True)),
                ('amount', models.FloatField(max_length=19)),
                ('currency', models.CharField(max_length=5)),
                ('txRef', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_date_time', models.DateTimeField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('gateway_response', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayStackCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('authorization_code', models.CharField(blank=True, max_length=100, null=True)),
                ('card_type', models.CharField(blank=True, max_length=10, null=True)),
                ('last4', models.CharField(blank=True, max_length=4, null=True)),
                ('exp_month', models.CharField(blank=True, max_length=10, null=True)),
                ('exp_year', models.CharField(blank=True, max_length=10, null=True)),
                ('bin', models.CharField(blank=True, max_length=10, null=True)),
                ('bank', models.CharField(blank=True, max_length=100, null=True)),
                ('account_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
