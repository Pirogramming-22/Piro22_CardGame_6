# Generated by Django 5.1.5 on 2025-01-16 10:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='attacker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attacker_games', to=settings.AUTH_USER_MODEL, verbose_name='공격자'),
        ),
        migrations.AddField(
            model_name='game',
            name='defender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defender_games', to=settings.AUTH_USER_MODEL, verbose_name='방어자'),
        ),
    ]
