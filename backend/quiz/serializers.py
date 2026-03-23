from rest_framework import serializers
from .models import Quiz, Question, QuizAttempt


class QuestionSerializer(serializers.ModelSerializer):
    """For active quiz — no correct answer revealed."""
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'hint', 'difficulty_score']


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d',
                  'correct_option', 'hint', 'explanation', 'difficulty_score']


class QuizListSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'difficulty', 'topic',
                  'user_type', 'level', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'difficulty', 'topic', 'user_type', 'level', 'questions']


class SubmitAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = serializers.DictField(child=serializers.CharField())


class QuizAttemptSerializer(serializers.ModelSerializer):
    percentage = serializers.FloatField(read_only=True, source='percentage')
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    quiz_user_type = serializers.CharField(source='quiz.user_type', read_only=True)
    quiz_level = serializers.IntegerField(source='quiz.level', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'quiz_title', 'quiz_user_type', 'quiz_level',
                  'score', 'total_questions', 'percentage', 'xp_earned',
                  'stars', 'hearts_lost', 'max_streak', 'difficulty_level', 'completed_at']
