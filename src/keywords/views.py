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

def keywords(request):
    return render(request, 'keywords/key_main.html')


def generate_wordcloud(text):
    # 텍스트를 형태소로 분석하여 단어 추출
    okt = Okt()
    nouns = okt.nouns(text)
    words = [n for n in nouns if len(n) > 1]  # 단어의 길이가 1개인 것은 제외

    count = Counter(words)

    # 워드클라우드 생성
    im = Image.open('keywords/image/heart.png')
    mask_arr = np.array(im)
    font_path = 'keywords/image/Font/malgunbd.ttf'
    wordcloud = WordCloud(font_path=font_path, width=50, mask=mask_arr, height=50, scale=2.0, max_font_size=250,
                          background_color='white').generate_from_frequencies(count)

    # 이미지 데이터 생성
    image_data = BytesIO()
    wordcloud.to_image().save(image_data, format='PNG')
    image_data.seek(0)
    encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

    return encoded_image


def wordcloud_view(request):
    # 텍스트 데이터 가져오기 (데이터베이스에서 가져오는 예시)
    # 여기서는 임의의 텍스트 데이터를 사용합니다.
    try:
        con = pymysql.connect(host='52.78.176.120', user='root', password='encore',
                              port=3306, db='gorogoro', charset='utf8')
        cur = con.cursor()
    except Exception as e:
        print(e)
    cur.execute("select * from api_feed")
    rows = cur.fetchall()
    text = ' '.join([i[1] for i in rows]).replace(",", " ")
    # text = "한국어 자연어 처리를 위해 KoNLPy와 Okt를 사용합니다."

    # 워드클라우드 생성 및 이미지 데이터 반환
    image_data = generate_wordcloud(text)

    # 이미지 데이터를 템플릿으로 전달하여 렌더링
    return render(request, 'keywords/key_main.html', {'image_data': image_data})