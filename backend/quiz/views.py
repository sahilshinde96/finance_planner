from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quiz, Question, QuizAttempt
from .serializers import (
    QuizListSerializer, QuizDetailSerializer,
    SubmitAnswerSerializer, QuizAttemptSerializer
)
from .adaptive import get_recommended_difficulty


class QuizListView(generics.ListAPIView):
    """List all active quizzes with optional filtering."""
    serializer_class = QuizListSerializer

    def get_queryset(self):
        qs = Quiz.objects.filter(is_active=True)
        difficulty = self.request.query_params.get('difficulty')
        user_type = self.request.query_params.get('user_type')
        topic = self.request.query_params.get('topic')
        level = self.request.query_params.get('level')
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if user_type:
            qs = qs.filter(user_type=user_type)
        if topic:
            qs = qs.filter(topic__icontains=topic)
        if level:
            qs = qs.filter(level=level)
        return qs.order_by('user_type', 'level')


class QuizDetailView(generics.RetrieveAPIView):
    """Get quiz with questions (answers hidden)."""
    serializer_class = QuizDetailSerializer
    queryset = Quiz.objects.filter(is_active=True)


class SubmitQuizView(APIView):
    """
    Submit quiz answers and return gamified results.
    XP Formula: (correct * 10) + (max_streak * 5)
    Stars: >=90% = 3, >=60% = 2, >=30% = 1, <30% = 0
    Hearts: start with 3, lose 1 per wrong answer
    """
    def post(self, request):
        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz_id = serializer.validated_data['quiz_id']
        answers = serializer.validated_data['answers']  # {"question_id": "A/B/C/D"}

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=404)

        questions = list(quiz.questions.all())
        score = 0
        hearts_lost = 0
        current_streak = 0
        max_streak = 0
        results = []

        for q in questions:
            user_answer = answers.get(str(q.id), '').upper()
            is_correct = user_answer == q.correct_option

            if is_correct:
                score += 1
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                hearts_lost += 1
                current_streak = 0

            results.append({
                'question_id': q.id,
                'question_text': q.text,
                'correct_option': q.correct_option,
                'user_answer': user_answer,
                'is_correct': is_correct,
                'hint': q.hint,
                'explanation': q.explanation,
            })

        total = len(questions)
        percentage = round((score / total) * 100, 1) if total > 0 else 0

        # Gamification calculations
        base_xp = score * 10
        streak_bonus = max_streak * 5
        xp_earned = base_xp + streak_bonus

        # Star rating
        if percentage >= 90:
            stars = 3
        elif percentage >= 60:
            stars = 2
        elif percentage >= 30:
            stars = 1
        else:
            stars = 0

        hearts_remaining = max(0, 3 - hearts_lost)

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total,
            xp_earned=xp_earned,
            stars=stars,
            hearts_lost=hearts_lost,
            max_streak=max_streak,
            difficulty_level=quiz.difficulty,
            answers=answers,
        )

        # Update streak total_points
        try:
            from streaks.models import Streak
            streak_obj, _ = Streak.objects.get_or_create(user=request.user)
            streak_obj.total_points += xp_earned
            streak_obj.save()
        except Exception:
            pass

        # Record blockchain block
        try:
            from blockchain.engine import create_block
            create_block(
                user=request.user,
                record_type='quiz_result',
                record_data={
                    'quiz_id': quiz.id,
                    'quiz_title': quiz.title,
                    'score': score,
                    'total': total,
                    'percentage': percentage,
                    'xp': xp_earned,
                    'stars': stars,
                }
            )
        except Exception:
            pass

        return Response({
            'attempt_id': attempt.id,
            'score': score,
            'total': total,
            'percentage': percentage,
            'xp_earned': xp_earned,
            'streak_bonus': streak_bonus,
            'stars': stars,
            'hearts_remaining': hearts_remaining,
            'hearts_lost': hearts_lost,
            'max_streak': max_streak,
            'results': results,
        })


class QuizHistoryView(generics.ListAPIView):
    """List user's quiz attempts."""
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).order_by('-completed_at')[:30]


class RecommendedDifficultyView(APIView):
    """Get recommended difficulty for the user."""
    def get(self, request):
        difficulty = get_recommended_difficulty(request.user)
        return Response({'recommended_difficulty': difficulty})


class QuizLeaderboardView(APIView):
    """Top users by XP from quizzes."""
    def get(self, request):
        from django.db.models import Sum, Count
        from django.contrib.auth import get_user_model
        User = get_user_model()

        top = (QuizAttempt.objects
               .values('user__username', 'user__id')
               .annotate(total_xp=Sum('xp_earned'), attempts=Count('id'), total_stars=Sum('stars'))
               .order_by('-total_xp')[:15])

        data = []
        for i, entry in enumerate(top):
            data.append({
                'rank': i + 1,
                'username': entry['user__username'],
                'total_xp': entry['total_xp'] or 0,
                'attempts': entry['attempts'],
                'total_stars': entry['total_stars'] or 0,
                'is_me': entry['user__id'] == request.user.id,
            })
        return Response(data)
