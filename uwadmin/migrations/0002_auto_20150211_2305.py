# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='connection',
            options={'ordering': ['con_src']},
        ),
        migrations.AlterModelOptions(
            name='connectiontype',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='langcode',
            options={'ordering': ['langcode']},
        ),
        migrations.AlterModelOptions(
            name='obspublishing',
            options={'ordering': ['lang']},
        ),
        migrations.AlterModelOptions(
            name='obstracking',
            options={'ordering': ['lang', 'contact']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='recentcommunication',
            options={'ordering': ['contact', 'created']},
        ),
        migrations.AlterField(
            model_name='connection',
            name='con_dst',
            field=models.ForeignKey(related_name='destination_connections', verbose_name=b'Connection', to='uwadmin.Contact'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='connection',
            name='con_src',
            field=models.ForeignKey(related_name='source_connections', to='uwadmin.Contact'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='languages',
            field=models.ManyToManyField(related_name='contacts', to='uwadmin.LangCode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='org',
            field=models.ManyToManyField(to='uwadmin.Organization', null=True, verbose_name=b'organizations', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='obspublishing',
            name='checking_entity',
            field=models.ManyToManyField(related_name='publications', to='uwadmin.Contact'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='obspublishing',
            name='lang',
            field=models.ForeignKey(related_name='publications', to='uwadmin.LangCode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='obstracking',
            name='contact',
            field=models.ForeignKey(related_name='tracking', to='uwadmin.Contact'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='obstracking',
            name='lang',
            field=models.ForeignKey(related_name='tracking', verbose_name=b'Language.', to='uwadmin.LangCode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='languages',
            field=models.ManyToManyField(related_name='organizations', to='uwadmin.LangCode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recentcommunication',
            name='contact',
            field=models.ForeignKey(related_name='recent_communications', to='uwadmin.Contact'),
            preserve_default=True,
        ),
    ]
