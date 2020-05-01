# Generated by Django 3.0.5 on 2020-04-30 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20200427_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='uploads/avatar/default.png', max_length=200, null=True, upload_to='avatar/%Y/%m', verbose_name='用户头像'),
        ),
    ]