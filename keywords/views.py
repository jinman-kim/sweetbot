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
    
    return render(request, 'keywords/wordcloud.html')

def generate_wordcloud(text):
    # 텍스트를 형태소로 분석하여 단어 추출
    okt = Okt()
    nouns = okt.nouns(text)
    words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

    count = Counter(words)

    # 워드클라우드 생성
    im = Image.open('image/다운로드.png')
    mask_arr = np.array(im)
    font_path = 'image/Font/malgunbd.ttf'
    wordcloud = WordCloud(font_path=font_path, width=50,mask = mask_arr, height=50, scale=2.0, max_font_size=250,
                background_color ='white').generate_from_frequencies(count)

    # 이미지 데이터 생성
    image_data = BytesIO()
    wordcloud.to_image().save(image_data, format='PNG')
    image_data.seek(0)
    encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

    return encoded_image

# 여기서 if문 써서 워드클라우드 보여줄지 안보여줄지 설정
# def wordcloud_view(request):
#     # 텍스트 데이터 가져오기 (데이터베이스에서 가져오는 예시)
#     # 여기서는 임의의 텍스트 데이터를 사용합니다.
#     try:
#         con = pymysql.connect(host='52.78.176.120', user='root', password='encore',  
#                           port=3306, db='gorogoro', charset='utf8')
#         cur = con.cursor()
#     except Exception as e:
#         print (e)
#     cur.execute("select * from api_feed where user_id='jin.99'")  # 해당 커플 id들의 워드 클라우드
#     rows = cur.fetchall()
#     text = ' '.join([i[1] for i in rows]).replace(",", " ")
#     # text = "한국어 자연어 처리를 위해 KoNLPy와 Okt를 사용합니다."

#     # 워드클라우드 생성 
#     image_data = generate_wordcloud(text)
    
#     image_path = os.path.join('wordcloud_img', 'wordcloud.png')
#     image_data.to_image().save(image_path, format='PNG')

#     return image_path
    # 이미지 데이터를 템플릿으로 전달하여 렌더링
    # return render(request, 'keywords/key_main.html', {'image_data': image_data})
    
    
def popular_keywords_view(request):
    # 인기 검색어 데이터 가져오기 (예시로 임의의 데이터 사용)
    popular_keywords = [
        # {'keyword': 'Python', 'count': 100},
        # {'keyword': 'Django', 'count': 80},
        # {'keyword': 'JavaScript', 'count': 70},
        # {'keyword': 'HTML', 'count': 60},
        # {'keyword': 'CSS', 'count': 50},
        {'keyword':'선물', 'count':613},
        {'keyword':'오늘', 'count':2},
        {'해산물', 2},
        {'다음', 2},
        {'안녕', 1},
        {'장고', 1},
        {'사랑', 1},
        {'횟집', 1}
    ]

    return render(request, 'keywords/pop.html', {'popular_keywords': popular_keywords})