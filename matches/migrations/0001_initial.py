# Generated by Django 2.1.2 on 2018-11-10 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipAddress', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ClientRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans_yes', models.PositiveIntegerField(default=0, null=True)),
                ('ans_no', models.PositiveIntegerField(default=0, null=True)),
                ('object1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a', to='matches.Object')),
                ('object2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='b', to='matches.Object')),
            ],
        ),
        migrations.AddField(
            model_name='clientrate',
            name='rates',
            field=models.ManyToManyField(to='matches.Rate'),
        ),
        migrations.AddField(
            model_name='addressrate',
            name='rates',
            field=models.ManyToManyField(to='matches.Rate'),
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together={('object1', 'object2')},
        ),
    ]
