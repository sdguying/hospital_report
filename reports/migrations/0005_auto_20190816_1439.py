# Generated by Django 2.2.4 on 2019-08-16 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20190816_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name_w',
            field=models.CharField(blank=True, max_length=200, verbose_name='科室大类'),
        ),
    ]