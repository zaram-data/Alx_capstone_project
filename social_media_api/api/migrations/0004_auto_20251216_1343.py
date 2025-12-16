

# In api/migrations/000X_auto_add_created_at_like.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_like_unique_together'),  # replace with last migration
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2025-01-01T00:00:00'),  # temporary default
            preserve_default=False,
        ),
    ]
