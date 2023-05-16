from django.shortcuts import render

# Create your views here.

#diary 페이지
def diary(request):
    
    return render(request, 'ourdiary/main.html')