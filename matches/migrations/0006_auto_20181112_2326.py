# Generated by Django 2.1.2 on 2018-11-12 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0005_auto_20181112_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
