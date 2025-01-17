# Generated by Django 5.1.5 on 2025-01-17 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_attacker_card_game_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='attacker',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='initiated_games', to=settings.AUTH_USER_MODEL),
        ),
    ]
