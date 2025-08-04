from django.shortcuts import render
from django.views import View

class HomeViews(View):
    template_name = 'home.html'
    
    def get(self, request):
        return render(request, 'home.html')
        
