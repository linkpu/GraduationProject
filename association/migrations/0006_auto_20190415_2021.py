# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-15 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0005_auto_20190414_0917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='activity_labelk',
            new_name='activity_label',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='activity_content',
        ),
        migrations.AddField(
            model_name='activity',
            name='join_fee',
            field=models.IntegerField(default=0, verbose_name='参与费用'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_conndition',
            field=models.IntegerField(choices=[(1, '直接加入'), (2, '缴费参与'), (3, '校内人员'), (4, '团内会员')], default=1, verbose_name='参与条件'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_status',
            field=models.IntegerField(choices=[(1, '已保存但未提交'), (2, '待审批'), (3, '待补充'), (4, '已通过审批'), (5, '未通过审批'), (6, '进行中'), (7, '已结束')], default=1, verbose_name='活动状态'),
        ),
    ]
