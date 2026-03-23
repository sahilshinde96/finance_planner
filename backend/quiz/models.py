from django.db import models
from django.conf import settings


class Quiz(models.Model):
    """A quiz module — organised by user_type and level."""
    DIFFICULTY_CHOICES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    USER_TYPE_CHOICES = [('farmer', 'Farmer'), ('corporate', 'Corporate'), ('general', 'General Public')]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    topic = models.CharField(max_length=100, default='general')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='general')
    level = models.PositiveIntegerField(default=1, help_text='1=Beginner, 2=Intermediate, 3=Advanced')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return f"[{self.user_type.upper()}] L{self.level} — {self.title}"


class Question(models.Model):
    """A question belonging to a quiz."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=400)
    option_b = models.CharField(max_length=400)
    option_c = models.CharField(max_length=400)
    option_d = models.CharField(max_length=400)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    hint = models.CharField(max_length=200, blank=True)
    explanation = models.TextField(blank=True)
    difficulty_score = models.PositiveIntegerField(default=1, help_text='1-10')

    def __str__(self):
        return self.text[:80]


class QuizAttempt(models.Model):
    """Records a user's quiz attempt with gamification data."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)        # correct answers count
    total_questions = models.PositiveIntegerField(default=0)
    xp_earned = models.PositiveIntegerField(default=0)    # XP points
    stars = models.PositiveIntegerField(default=0)        # 0-3 stars
    hearts_lost = models.PositiveIntegerField(default=0)  # hearts used (max 3)
    max_streak = models.PositiveIntegerField(default=0)   # longest consecutive streak
    difficulty_level = models.CharField(max_length=10, default='easy')
    answers = models.JSONField(default=dict, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100, 1)

    def __str__(self):
        return f"{self.user.username} — {self.quiz.title}: {self.score}/{self.total_questions} ({self.xp_earned} XP)"
