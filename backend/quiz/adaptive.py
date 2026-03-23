def get_recommended_difficulty(user):
    """Return recommended difficulty based on recent performance."""
    from .models import QuizAttempt
    recent = QuizAttempt.objects.filter(user=user).order_by('-completed_at')[:5]
    if not recent:
        return 'easy'
    avg_pct = sum(a.percentage() for a in recent) / len(recent)
    if avg_pct >= 80:
        return 'hard'
    elif avg_pct >= 55:
        return 'medium'
    return 'easy'
