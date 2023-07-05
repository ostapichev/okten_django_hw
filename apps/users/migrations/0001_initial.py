# Generated by Django 4.2.2 on 2023-06-30 08:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[А-ЯЁІЇЄ][а-яёіїґє]{1,49}$', 'This name must contain only Cyrillic characters.')])),
                ('surname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[А-ЯЁІЇЄ][а-яёіїґє]{1,49}$', 'This surname must contain only Cyrillic characters.')])),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxValueValidator(150)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, upload_to='image')),
            ],
            options={
                'db_table': 'profile',
                'ordering': ('id', 'name', 'surname', 'age'),
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[
                    django.core.validators.RegexValidator('^[\\w.%+-]+@gmail\\.com$',
                                                          'The email domain must be gmail.com')])),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[\\'`\\!@#$%\\^&\\*\\(\\)\\-_=\\+\\|\\\\\\/\\?\\.>,<])(?=.*\\S)[a-zA-Z\\d\\'`\\!@#$%\\^&\\*\\(\\)\\-_=\\+\\|\\\\\\/\\?\\.>,<]{8,30}$", 'This password must be at least one uppercase letter, at least one lowercase letter, at least one special character and at least one number min 8 max 30 characters.')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.profilemodel')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
                'ordering': ('id',),
            },
        ),
    ]
