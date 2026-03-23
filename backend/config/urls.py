"""ARTH — Root URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        'name': 'ARTH — Smart Financial Planning Platform API',
        'version': '2.0',
        'status': 'running ✅',
        'endpoints': {
            'accounts': '/api/accounts/',
            'chatbot': '/api/chatbot/',
            'quiz': '/api/quiz/',
            'streaks': '/api/streaks/',
            'schemes': '/api/schemes/',
            'planner': '/api/planner/',
            'blockchain': '/api/blockchain/',
        },
        'frontend': 'http://localhost:5173',
        'new_in_v2': [
            'ML Finance Planner at /api/planner/ml-plan/',
            'Quiz Leaderboard at /api/quiz/leaderboard/',
            'Gamified quiz (XP, hearts, stars)',
            '72 KnowQuest questions across 9 modules',
        ]
    })


urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/quiz/', include('quiz.urls')),
    path('api/streaks/', include('streaks.urls')),
    path('api/schemes/', include('schemes.urls')),
    path('api/planner/', include('planner.urls')),
    path('api/blockchain/', include('blockchain.urls')),
]
