# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_board', '0006_entry_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='owner',
        ),
    ]