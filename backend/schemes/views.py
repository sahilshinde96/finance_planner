from rest_framework import generics
from .models import GovernmentScheme
from .serializers import GovernmentSchemeSerializer

class SchemeListView(generics.ListAPIView):
    serializer_class = GovernmentSchemeSerializer
    def get_queryset(self):
        qs = GovernmentScheme.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs
