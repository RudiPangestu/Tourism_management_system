# Generated by Django 5.2.1 on 2025-05-20 04:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tours', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('number_of_people', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('special_requests', models.TextField(blank=True)),
                ('confirmation_code', models.CharField(max_length=50, unique=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tours.tour')),
                ('tour_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tours.tourdate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-booking_date'],
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('passport_number', models.CharField(blank=True, max_length=50)),
                ('nationality', models.CharField(max_length=100)),
                ('emergency_contact', models.CharField(max_length=100)),
                ('emergency_phone', models.CharField(max_length=20)),
                ('dietary_requirements', models.TextField(blank=True)),
                ('medical_conditions', models.TextField(blank=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='bookings.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer'), ('paypal', 'PayPal')], max_length=20)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('is_deposit', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='bookings.booking')),
            ],
        ),
    ]
