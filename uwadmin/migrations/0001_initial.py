# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('con_src',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConnectionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of Connection Type')),
                ('mutual', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of contact')),
                ('email', models.CharField(max_length=255, verbose_name=b'Email address', blank=True)),
                ('d43username', models.CharField(max_length=255, verbose_name=b'Door43 username', blank=True)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('phone', models.CharField(max_length=255, verbose_name=b'Phone number', blank=True)),
                ('other', models.TextField(verbose_name=b'Other information', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LangCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('langcode', models.CharField(unique=True, max_length=25, verbose_name=b'Language Code')),
                ('langname', models.CharField(max_length=255, verbose_name=b'Language Name')),
            ],
            options={
                'ordering': ('langcode',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OBSPublishing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publish_date', models.DateField()),
                ('version', models.CharField(max_length=10)),
                ('source_version', models.CharField(max_length=10)),
                ('checking_level', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3')])),
                ('comments', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('checking_entity', models.ManyToManyField(related_name='OBSPublishing', to='uwadmin.Contact')),
                ('contributors', models.ManyToManyField(to='uwadmin.Contact')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('lang', models.ForeignKey(related_name='OBSPublishing', to='uwadmin.LangCode')),
                ('source_text', models.ForeignKey(to='uwadmin.LangCode')),
            ],
            options={
                'ordering': ('lang',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OBSTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_started', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contact', models.ForeignKey(related_name='OBSTracking', to='uwadmin.Contact')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('lang', models.ForeignKey(related_name='OBSTracking', verbose_name=b'Language.', to='uwadmin.LangCode')),
            ],
            options={
                'ordering': ('lang', 'contact'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of Organization')),
                ('email', models.CharField(max_length=255, verbose_name=b'Email address', blank=True)),
                ('phone', models.CharField(max_length=255, verbose_name=b'Phone number', blank=True)),
                ('website', models.CharField(max_length=255, blank=True)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('other', models.TextField(verbose_name=b'Other information', blank=True)),
                ('checking_entity', models.BooleanField(default=False)),
                ('languages', models.ManyToManyField(related_name='Organization', to='uwadmin.LangCode')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecentCommunication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('communication', models.TextField(verbose_name=b'Message', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contact', models.ForeignKey(related_name='RecentCommunication', to='uwadmin.Contact')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('contact', 'created'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contact',
            name='languages',
            field=models.ManyToManyField(related_name='Contact', to='uwadmin.LangCode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='org',
            field=models.ManyToManyField(to='uwadmin.Organization', null=True, verbose_name=b'Organization', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='con_dst',
            field=models.ForeignKey(verbose_name=b'Connection', to='uwadmin.Contact'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='con_src',
            field=models.ForeignKey(related_name='Connection', to='uwadmin.Contact'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='con_type',
            field=models.ForeignKey(verbose_name=b'Type', to='uwadmin.ConnectionType'),
            preserve_default=True,
        ),
    ]
