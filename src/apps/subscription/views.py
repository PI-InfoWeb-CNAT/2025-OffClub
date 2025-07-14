from django.shortcuts import render

class PlansViews:
    @staticmethod
    def plans(request):
        return render(request, 'plans.html')
    
    