# Generated by Django 2.1.2 on 2018-11-13 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0008_dateanswer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dateanswer',
            old_name='created',
            new_name='date',
        ),
    ]
