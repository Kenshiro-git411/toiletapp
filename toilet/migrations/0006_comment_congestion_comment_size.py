# Generated by Django 5.1.6 on 2025-04-07 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toilet', '0005_femaletoilet_congestion_femaletoilet_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='congestion',
            field=models.IntegerField(help_text='5段階で数値を入力してください', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='size',
            field=models.IntegerField(help_text='5段階で数値を入力してください', null=True),
        ),
    ]
