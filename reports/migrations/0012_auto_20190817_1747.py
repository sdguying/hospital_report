# Generated by Django 2.2.4 on 2019-08-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_auto_20190817_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tips',
            field=models.CharField(blank=True, choices=[('↑', '↑'), ('↓', '↓')], max_length=10, verbose_name='提示'),
        ),
    ]
