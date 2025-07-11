from django.shortcuts import render

# Create your views here.
def offer(request):
    return render(request, 'offer_detail.html')