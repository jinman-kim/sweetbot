from django.shortcuts import render

# Create your views here.

def love_profile(request):
    
    return render(request, 'love_profile/lp_main.html')