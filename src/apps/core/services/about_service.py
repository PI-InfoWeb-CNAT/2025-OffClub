from ...enterprise.models import Enterprise
from ...subscriber.models import Subscriber
from django.utils import timezone
from django.core.paginator import Paginator

class AboutService():
    @staticmethod
    def about_page_context():
        count_enterprises = Enterprise.objects.all().count()
        count_subscribers = Subscriber.objects.all().count()
        context = {
            'count_enterprises': count_enterprises, 
            'count_subscribers': count_subscribers,
        }
        return context
    