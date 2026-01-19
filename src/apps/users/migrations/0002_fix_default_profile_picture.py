from django.db import migrations


def forwards(apps, schema_editor):
    User = apps.get_model('users', 'User')
    users = User.objects.filter(profile_picture__startswith='static/')
    for u in users:
        u.profile_picture = None
        u.save(update_fields=['profile_picture'])


def reverse(apps, schema_editor):
    User = apps.get_model('users', 'User')
    users = User.objects.filter(profile_picture__isnull=True)
    for u in users:
        u.profile_picture = 'static/imgs/default-profile-picture.png'
        u.save(update_fields=['profile_picture'])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
