# Generated by Django 2.0 on 2020-04-12 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200408_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='head_image/%Y/%m', verbose_name='用户头像'),
        ),
    ]
