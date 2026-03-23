from rest_framework import serializers
from .models import HashBlock

class HashBlockSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    class Meta:
        model = HashBlock
        fields = ['id', 'block_index', 'record_type', 'record_data',
                  'hash', 'previous_hash', 'timestamp', 'is_valid']
