from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=10, default='🏆')),
                ('requirement', models.CharField(max_length=200)),
                ('points_value', models.PositiveIntegerField(default=50)),
                ('badge_type', models.CharField(max_length=20, default='achievement')),
            ],
        ),
        migrations.CreateModel(
            name='Streak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('current_streak', models.PositiveIntegerField(default=0)),
                ('longest_streak', models.PositiveIntegerField(default=0)),
                ('total_points', models.PositiveIntegerField(default=0)),
                ('last_activity_date', models.DateField(null=True, blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='streak', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streaks.badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badges', to=settings.AUTH_USER_MODEL)),
            ],
            options={'unique_together': {('user', 'badge')}},
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('activity_type', models.CharField(max_length=50)),
                ('points_earned', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'unique_together': {('user', 'date', 'activity_type')}, 'ordering': ['-date']},
        ),
    ]
