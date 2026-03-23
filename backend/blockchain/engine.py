import hashlib, json
from django.utils import timezone
from .models import HashBlock

def create_block(user, record_type: str, record_data: dict):
    last = HashBlock.objects.filter(user=user).order_by('-block_index').first()
    prev_hash = last.hash if last else '0' * 64
    index = (last.block_index + 1) if last else 1
    now = timezone.now()
    data_str = json.dumps(record_data, sort_keys=True)
    hash_val = hashlib.sha256(
        f"{index}{prev_hash}{data_str}{now.isoformat()}".encode()
    ).hexdigest()
    return HashBlock.objects.create(
        user=user, block_index=index, record_type=record_type,
        record_data=record_data, hash=hash_val, previous_hash=prev_hash, timestamp=now
    )
