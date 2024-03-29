# Generated by Django 5.0.2 on 2024-02-11 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_api', '0003_item_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(default='NULL', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='availableStock',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='currentStock',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='tag',
            field=models.CharField(default='NULL', max_length=100),
        ),
    ]
