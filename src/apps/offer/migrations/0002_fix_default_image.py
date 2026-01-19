from django.db import migrations


def forwards(apps, schema_editor):
    Offer = apps.get_model('offer', 'Offer')
    # Set image to None for any offers whose image points to static/ (was a bad default)
    offers = Offer.objects.filter(image__startswith='static/')
    for offer in offers:
        offer.image = None
        offer.save(update_fields=['image'])


def reverse(apps, schema_editor):
    Offer = apps.get_model('offer', 'Offer')
    # Restore previous default for reverse migration if needed
    offers = Offer.objects.filter(image__isnull=True)
    for offer in offers:
        offer.image = 'static/imgs/default-offer-image.png'
        offer.save(update_fields=['image'])


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
