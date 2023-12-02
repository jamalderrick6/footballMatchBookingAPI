# Generated by Django 4.2.7 on 2023-12-01 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0004_alter_stadium_hash_value_alter_team_hash_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderId', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.match')),
            ],
            options={
                'db_table': 'order',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(max_length=100)),
                ('ticketNumber', models.CharField(max_length=255, unique=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='game.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reservation',
                'managed': True,
            },
        ),
    ]