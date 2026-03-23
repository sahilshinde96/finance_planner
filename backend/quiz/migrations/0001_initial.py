from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('difficulty', models.CharField(max_length=10, default='easy')),
                ('topic', models.CharField(max_length=100, default='general')),
                ('user_type', models.CharField(max_length=20, default='general')),
                ('level', models.PositiveIntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('option_a', models.CharField(max_length=400)),
                ('option_b', models.CharField(max_length=400)),
                ('option_c', models.CharField(max_length=400)),
                ('option_d', models.CharField(max_length=400)),
                ('correct_option', models.CharField(max_length=1)),
                ('hint', models.CharField(max_length=200, blank=True)),
                ('explanation', models.TextField(blank=True)),
                ('difficulty_score', models.PositiveIntegerField(default=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('total_questions', models.PositiveIntegerField(default=0)),
                ('xp_earned', models.PositiveIntegerField(default=0)),
                ('stars', models.PositiveIntegerField(default=0)),
                ('hearts_lost', models.PositiveIntegerField(default=0)),
                ('max_streak', models.PositiveIntegerField(default=0)),
                ('difficulty_level', models.CharField(max_length=10, default='easy')),
                ('answers', models.JSONField(default=dict, blank=True)),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='quiz.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_attempts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
