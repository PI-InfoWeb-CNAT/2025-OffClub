from django.shortcuts import render
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
# from apps.users.forms import EnterpriseSignUpForm

class EnterpriseDashboardView(View):
    template_name = 'enterprise_dashboard.html'
    
    def get(self, request):
        return render(request, 'enterprise_dashboard.html')


# class EnterpriseSignUpView(CreateView):
#     """
#     Renderiza e processa o formulário de registro para novas empresas.
#     """
#     form_class = EnterpriseSignUpForm
#     template_name = 'registration/signup_form.html'
    
#     sucess_url = reverse_lazy('enterprise_signup_done')
    
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'enterprise'
#         return super().get_context_data(**kwargs)
    
# def enterprise_signup_done(request):
#     """
#     Página de sucesso exibida após o registro bem sucedido.
#     """
#     return render(request, 'registration/signup_done.html')