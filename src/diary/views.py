
# Create your views here.
from django.shortcuts import render
from api.models import Feed
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from chat.settings import MEDIA_ROOT
from django.shortcuts import render, redirect
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


# Create your views here.


# diary 페이지
class Main(APIView):
    @method_decorator(login_required(login_url='user:login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')
        return render(request, 'ourdiary/main.html', context=dict(feed_list=feed_list))


class UploadFeed(APIView):
    @method_decorator(login_required(login_url='user:login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        print("upload 실행")
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')
        image = uuid_name
        profile_image = request.data.get('profile_image')
        user_id = request.data.get('user_id')

        Feed.objects.create(content=content, image=image, profile_image=profile_image, user_id=user_id, like_count=0)

        return Response(status=200)