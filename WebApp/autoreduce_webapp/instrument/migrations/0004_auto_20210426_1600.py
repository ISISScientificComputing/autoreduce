# Generated by Django 3.1.2 on 2021-04-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0003_merge_20210426_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variable',
            name='value',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
