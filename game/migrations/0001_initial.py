# Generated by Django 4.2.7 on 2023-11-30 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('image', models.CharField(blank=True, max_length=200)),
                ('hash_value', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'stadium',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('hash_value', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'team',
                'managed': True,
            },
        ),
    ]
