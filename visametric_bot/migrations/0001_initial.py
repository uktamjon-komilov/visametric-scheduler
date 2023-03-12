# Generated by Django 4.1.7 on 2023-03-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('nationality', models.CharField(choices=[('Uzbekistan', 'Uzbekistan'), ('Special', 'Special'), ('Foreign', 'Foreign')], max_length=25)),
                ('address', models.CharField(choices=[('Andijan', 'Andijan'), ('Angren', 'Angren'), ('Bekobod', 'Bekobod'), ('Bukhara', 'Bukhara'), ('Chirchiq', 'Chirchiq'), ('Fergana', 'Fergana'), ('Jizzakh', 'Jizzakh'), ('Kokand', 'Kokand'), ('Margilan', 'Margilan'), ('Namangan', 'Namangan'), ('Navoiy', 'Navoiy'), ('Nukus', 'Nukus'), ('Olmaliq', 'Olmaliq'), ('Qarshi', 'Qarshi'), ('Samarkand', 'Samarkand'), ('Shahrisabz', 'Shahrisabz'), ('Tashkent', 'Tashkent'), ('Termez', 'Termez'), ('Urgench', 'Urgench')], max_length=25)),
                ('passport_number', models.CharField(max_length=25)),
                ('phone_number', models.CharField(max_length=12)),
                ('plan', models.CharField(choices=[('monthly', 'Monthly'), ('express', 'Express')], default='monthly', max_length=20)),
                ('birth_date', models.DateField()),
                ('passport_valid_date', models.DateField()),
                ('is_registered', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('url_for_document', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=20, unique=True)),
                ('state', models.CharField(choices=[('start', 'start'), ('monthly_plan', 'monthly plan'), ('express_plan', 'express plan'), ('get_first_name', 'get first name'), ('get_last_name', 'get last name'), ('get_passport_number', 'get passport number'), ('get_passport_valid_date', 'get passport valid date'), ('get_nationality', 'get nationality'), ('get_address', 'get address'), ('get_birth_date', 'get birth date'), ('get_email', 'get email'), ('get_phone_number', 'get phone number'), ('edit_first_name', 'edit first name'), ('edit_last_name', 'edit last name'), ('edit_passport_number', 'edit passport number'), ('edit_passport_valid_date', 'edit passport valid date'), ('edit_nationality', 'edit nationality'), ('edit_address', 'edit address'), ('edit_birth_date', 'edit birth date'), ('edit_email', 'edit email'), ('edit_phone_number', 'edit phone number')], max_length=35)),
            ],
        ),
    ]