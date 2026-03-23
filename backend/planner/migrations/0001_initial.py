from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='FinancialGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('target_amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('current_amount', models.DecimalField(max_digits=12, decimal_places=2, default=0)),
                ('target_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(max_length=20, default='active')),
                ('priority', models.CharField(max_length=10, default='medium')),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_goals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
