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
from django.shortcuts import render
from django.db import connection
from collections import Counter
from wordcloud import WordCloud
from konlpy.tag import Okt
from PIL import Image
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import pymysql


# Create your views here.

# def generate_wordcloud(text):
#     # 텍스트를 형태소로 분석하여 단어 추출
#     okt = Okt()
#     nouns = okt.nouns(text)
#     words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

#     count = Counter(words)

#     # 워드클라우드 생성
#     im = Image.open('image/다운로드.png')
#     mask_arr = np.array(im)
#     font_path = 'image/Font/malgunbd.ttf'
#     wordcloud = WordCloud(font_path=font_path, width=50,mask = mask_arr, height=50, scale=2.0, max_font_size=250,
#                 background_color ='white').generate_from_frequencies(count)

#     # 이미지 데이터 생성
#     image_data = BytesIO()
#     wordcloud.to_image().save(image_data, format='PNG')
#     image_data.seek(0)
#     encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

#     return encoded_image

# def wordcloud_view(request):
#     try:
#         con = pymysql.connect(host='52.78.176.120', user='root', password='encore',  
#                             port=3306, db='gorogoro', charset='utf8')
#         cur = con.cursor()
#         cur.execute("select * from api_feed")
#         rows = cur.fetchall()
#         text = ' '.join([i[1] for i in rows]).replace(",", " ")
#         image_data = generate_wordcloud(text)
#     except Exception as e:
#         print(e)
#         image_data = None
#     return render(request, 'ourdiary/word.html', {'image_data': image_data})




#diary 페이지
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
    
