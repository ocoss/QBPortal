# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-21 00:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff_portal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('SC', 'SC'), ('NC', 'NC')], max_length=2)),
                ('zip_code', models.CharField(max_length=15)),
                ('phone_number', models.CharField(max_length=20)),
                ('rep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff_portal.StaffMember', verbose_name='323 Sports Representative')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
