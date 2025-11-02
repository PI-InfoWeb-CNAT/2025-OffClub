from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView 
from apps.enterprise.models import Enterprise, LineOfBusiness
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from .services import EnterpriseRequestService
from django.db.models import Q

class EnterpriseRequestsView(ListView):
    model = Enterprise 
    template_name = 'admin_user.html'
    paginate_by = 6 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.all()
        context['lines_of_business'] = LineOfBusiness.objects.all()
        context['enterprisesCount'] = context['paginator'].count
        # Lista dos ids dos ramos de empresa
        context['selected_lob_ids'] = self.request.GET.getlist('lines_of_business')
        
        return context

    def get_queryset(self):        
        queryset = super().get_queryset()
        queryset = queryset.filter(user__is_active=False)
        name = self.request.GET.get('name', None)
        lob_ids = self.request.GET.getlist('lines_of_business')
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)      

        if name:
            # Busca na Razão Social E no Nome Fantasia
            queryset = queryset.filter(
                Q(corporate_reason__icontains=name) | 
                Q(trade_name__icontains=name)
            )

        if lob_ids:
            queryset = queryset.filter(line_of_business__id__in=lob_ids).distinct()

        if start_date:
            queryset = queryset.filter(user__date_joined__gte=start_date)

        if end_date:
            queryset = queryset.filter(user__date_joined__lte=end_date)

        return queryset.order_by('-user__date_joined')

class EnterpriseRequestDetailView(DetailView):
    model = Enterprise 
    template_name = 'enterprise_request_detail.html'
    context_object_name = 'enterprise'

class EnterpriseRequestProcessView(View):
    def post(self, request, pk):
        enterprise = get_object_or_404(Enterprise, pk=pk)
        action = request.POST.get('action')

        try:
            if action == 'approve':
                EnterpriseRequestService.approve(enterprise)
                messages.success(request, f"A empresa '{enterprise.trade_name}' foi aprovada com sucesso.")
            
            elif action == 'deny':
                user_identifier = enterprise.user.email or f"ID {enterprise.user.pk}"
                EnterpriseRequestService.deny(enterprise) 
                messages.success(request, f"A solicitação de '{user_identifier}' foi recusada e excluída.")
                
            elif action == 'review':
                EnterpriseRequestService.request_review(enterprise)
                messages.info(request, "Ação 'Solicitar Revisão' registrada.")
        
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar a solicitação: {e}")

        return redirect('enterprises_requests')
    
    def get(self, request, pk):
        return redirect('enterprises_requests')
