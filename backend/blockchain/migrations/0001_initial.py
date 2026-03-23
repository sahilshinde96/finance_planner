from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='HashBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('block_index', models.PositiveIntegerField()),
                ('record_type', models.CharField(max_length=50)),
                ('record_data', models.JSONField()),
                ('hash', models.CharField(max_length=64)),
                ('previous_hash', models.CharField(max_length=64, default='0'*64)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blockchain_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-block_index']},
        ),
    ]
