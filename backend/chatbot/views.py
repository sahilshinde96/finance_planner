from rest_framework.views import APIView
from rest_framework.response import Response
from .ml_engine import get_response


class ChatMessageView(APIView):
    def post(self, request):
        message = request.data.get('message', '').strip()
        if not message:
            return Response({'error': 'Message required'}, status=400)
        response = get_response(message)
        return Response({'response': response, 'message': response})
