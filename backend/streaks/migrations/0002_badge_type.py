from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='badge_type',
            field=models.CharField(
                choices=[('quiz', 'Quiz'), ('streak', 'Streak'), ('achievement', 'Achievement'), ('feature', 'Feature')],
                default='achievement', max_length=20
            ),
        ),
    ]
