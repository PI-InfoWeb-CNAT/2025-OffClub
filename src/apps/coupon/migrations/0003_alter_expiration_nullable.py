from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("coupon", "0002_alter_code_unique"),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de Expiração do Cupom'),
        ),
    ]
