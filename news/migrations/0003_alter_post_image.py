# Generated by Django 4.2.7 on 2023-12-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_post_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(max_length=1000),
        ),
    ]
