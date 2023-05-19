from django.shortcuts import render, redirect

def index(request):
    print("에러")
    return render(request, 'index.html')