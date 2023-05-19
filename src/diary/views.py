from django.shortcuts import render
from .models import Feed
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from chat.settings import MEDIA_ROOT
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import timedelta
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import openai
import threading
import time
import os
import uuid
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.models import User

# Create your views here.




#diary 페이지
class Main(APIView):
    @method_decorator(login_required(login_url='user:login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')
        user_list = User.objects.all()
        return render(request, 'ourdiary/main.html', context={'feed_list': feed_list, 'user_list': user_list})
    

class UploadFeed(APIView):
    def post(self, request):
        print("upload 실행")
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')
        email = request.data.get('email')
        image = uuid_name
        # profile_image = request.data.get('User.thumbnail')
        print(request.user)
        user_id = request.user

        Feed.objects.create(content=content, image=image, user_id=user_id)

        return Response(status=200)


class DeleteFeed(APIView):
    def delete(self, request, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        print(type(feed.user_id))
        print(type(request.user))
        if feed.user_id != str(request.user):
            return Response(status=403)  # Forbidden
        else:
            feed.delete()
        return Response(status=204)  # No content
    
    