# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SudokuImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sudoku_img/%Y/%m/%d/')),
            ],
        ),
    ]
