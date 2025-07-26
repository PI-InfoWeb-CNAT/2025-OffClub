from django.shortcuts import render
from django.views import View
from .models import SubscriptionPlan, Feature

class SubscriptionPlanView(View):
    template_name = 'plans.html'

    def get(self, request):
        plans = SubscriptionPlan.objects.all().prefetch_related('features').order_by('price')
        all_features = Feature.objects.all()

        context = {
            'plans': plans,
            'all_features': all_features,
        }

        return render(request, self.template_name, context)
    