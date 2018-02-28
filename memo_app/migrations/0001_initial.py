# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 06:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Memos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_column='제목', max_length=50)),
                ('text', models.TextField(db_column='내용', help_text='메모 내용은 230자 이내로 입력 가능합니다.', max_length=230)),
                ('update_date', models.DateTimeField()),
                ('priority', models.BooleanField(db_column='중요')),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('name_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
