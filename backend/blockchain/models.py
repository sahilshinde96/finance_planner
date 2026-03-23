import hashlib
import json
from django.db import models
from django.conf import settings
from django.utils import timezone


class HashBlock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blockchain_records')
    block_index = models.PositiveIntegerField()
    record_type = models.CharField(max_length=50)
    record_data = models.JSONField()
    hash = models.CharField(max_length=64)
    previous_hash = models.CharField(max_length=64, default='0' * 64)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-block_index']

    @property
    def is_valid(self):
        data_str = json.dumps(self.record_data, sort_keys=True)
        computed = hashlib.sha256(
            f"{self.block_index}{self.previous_hash}{data_str}{self.timestamp.isoformat()}".encode()
        ).hexdigest()
        return computed == self.hash

    def __str__(self):
        return f"Block #{self.block_index} — {self.record_type} ({self.user.username})"
