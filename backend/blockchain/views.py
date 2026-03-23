from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HashBlock
from .serializers import HashBlockSerializer

class BlockchainRecordsView(generics.ListAPIView):
    serializer_class = HashBlockSerializer
    def get_queryset(self):
        return HashBlock.objects.filter(user=self.request.user).order_by('-block_index')[:50]

class VerifyChainView(APIView):
    def get(self, request):
        blocks = list(HashBlock.objects.filter(user=request.user).order_by('block_index'))
        for i, block in enumerate(blocks):
            if not block.is_valid:
                return Response({'is_valid': False, 'failed_at': block.block_index})
            if i > 0 and block.previous_hash != blocks[i-1].hash:
                return Response({'is_valid': False, 'failed_at': block.block_index})
        return Response({'is_valid': True, 'total_blocks': len(blocks)})
