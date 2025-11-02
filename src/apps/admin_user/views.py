from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from apps.enterprise.models import Enterprise, LineOfBusiness 

class EnterpriseRequestsView(ListView):
    model = Enterprise 
    template_name = 'admin_user.html'
    paginate_by = 6 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()
        context['lines_of_business'] = LineOfBusiness.objects.all()
        context['enterprisesCount'] = context['paginator'].count
        
        return context

    def get_queryset(self):        
        queryset = super().get_queryset()
        queryset = queryset.filter(user__is_active=False)      
        return queryset.order_by('-user__date_joined')

class EnterpriseRequestDetailView(DetailView):
    model = Enterprise 
    template_name = 'enterprise_request_detail.html'
    context_object_name = 'enterprise'
