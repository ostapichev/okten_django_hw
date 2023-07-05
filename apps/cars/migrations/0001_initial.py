# Generated by Django 4.2.2 on 2023-06-28 16:42

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auto_parks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('brand', models.CharField(max_length=25, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z\\d]{1,24}$', 'First letter uppercase min 2 max 24 ch')])),
                ('body', models.CharField(choices=[('Hatchback', 'Hatchback'), ('Sedan', 'Sedan'), ('MUV / SUV', 'Muv Suv'), ('Coupe', 'Coupe'), ('Convertible', 'Convertible'), ('Wagon', 'Wagon'), ('Van', 'Van'), ('Jeep', 'Jeep')], max_length=11)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)])),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2023)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auto_park', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='auto_parks.autoparkmodel')),
            ],
            options={
                'db_table': 'cars',
                'ordering': ('id',),
            },
        ),
    ]
