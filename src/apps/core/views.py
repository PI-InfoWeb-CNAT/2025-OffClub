from django.shortcuts import render
from .services.about_service import AboutService
from django.views import View

class HomeViews(View):
    template_name = 'home.html'
    
    def get(self, request):
        return render(request, 'home.html')

class AboutViews(View):
    template_name = 'about.html'
    
    def get(self, request):
        context = AboutService.about_page_context()
        return render(request, 'about.html', context = context)
        
