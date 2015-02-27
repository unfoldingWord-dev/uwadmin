# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uwadmin', '0003_obstracking_offline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenBibleStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_started', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('offline', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('publish_date', models.DateField(null=True, blank=True)),
                ('version', models.CharField(max_length=10, blank=True)),
                ('source_version', models.CharField(max_length=10, blank=True)),
                ('checking_level', models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2'), (3, b'3')])),
                ('checking_entity', models.ManyToManyField(related_name='resource_publications', to='uwadmin.Contact', blank=True)),
                ('contact', models.ForeignKey(related_name='resources', to='uwadmin.Contact')),
                ('contributors', models.ManyToManyField(related_name='+', to='uwadmin.Contact', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('lang', models.ForeignKey(related_name='resources', verbose_name=b'Language.', to='uwadmin.LangCode')),
                ('source_text', models.ForeignKey(related_name='+', blank=True, to='uwadmin.LangCode', null=True)),
            ],
            options={
                'ordering': ['lang', 'contact'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='open_bible_story',
            field=models.ForeignKey(related_name='comments', to='uwadmin.OpenBibleStory'),
            preserve_default=True,
        ),
    ]
