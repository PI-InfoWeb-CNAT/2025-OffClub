# Generated migration to set code length to 7 and unique
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coupon", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="code",
            field=models.CharField(max_length=7, unique=True, verbose_name="Código"),
        ),
    ]
