# Generated by Django 3.2.18 on 2023-04-19 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVisitHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=255)),
                ('referer', models.CharField(blank=True, max_length=255, null=True)),
                ('user_agent', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User visit history',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='LoginHistoryTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('successful', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Login history trail',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='LoginAttemptsHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('successful', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Login attempts history',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ExtraData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('browser', models.CharField(max_length=255)),
                ('ip_address', models.GenericIPAddressField()),
                ('device', models.CharField(blank=True, max_length=255, null=True)),
                ('os', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Extra data',
                'ordering': ['-timestamp'],
            },
        ),
    ]