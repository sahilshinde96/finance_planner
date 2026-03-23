from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='GovernmentScheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=20)),
                ('benefits', models.TextField()),
                ('eligibility_criteria', models.TextField()),
                ('min_age', models.PositiveIntegerField(null=True, blank=True)),
                ('max_age', models.PositiveIntegerField(null=True, blank=True)),
                ('max_income', models.PositiveIntegerField(null=True, blank=True)),
                ('state', models.CharField(max_length=100, default='All India')),
                ('applicable_categories', models.CharField(max_length=200, default='General,SC,ST,OBC')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
