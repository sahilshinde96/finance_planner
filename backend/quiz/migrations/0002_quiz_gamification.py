from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='user_type',
            field=models.CharField(
                choices=[('farmer', 'Farmer'), ('corporate', 'Corporate'), ('general', 'General Public')],
                default='general', max_length=20
            ),
        ),
        migrations.AddField(
            model_name='quiz',
            name='level',
            field=models.PositiveIntegerField(default=1, help_text='1=Beginner, 2=Intermediate, 3=Advanced'),
        ),
        migrations.AddField(
            model_name='question',
            name='hint',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='xp_earned',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='stars',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='hearts_lost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='max_streak',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
