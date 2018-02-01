# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='departmen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Documents.Department', verbose_name='Отдел'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100, verbose_name='Пароль'),
        ),
    ]