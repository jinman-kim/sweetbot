from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import os
import pymysql

def generate_wordclouds(host, user, password, port, db, charset, user_ids, mask_image_path, font_path):
    try:
        con = pymysql.connect(host=host, user=user, password=password, port=port, db=db, charset=charset)
        cur = con.cursor()
    except Exception as e:
        print(e)
        return
    
    for user_id in user_ids:
        cur.execute("SELECT * FROM api_feed WHERE user_id=%s", (user_id,))
        rows = cur.fetchall()
        text = ' '.join([i[1] for i in rows]).replace(",", " ")

        mask_image = Image.open(mask_image_path)
        mask_arr = np.array(mask_image)

        okt = Okt()
        nouns = okt.nouns(text)

        words = [n for n in nouns if len(n) > 1]

        word_counts = Counter(words)

        wc = WordCloud(font_path=font_path, width=400, mask=mask_arr, height=400, scale=2.0, max_font_size=250,
                       background_color='#F7F7F7')
        wordcloud_gen = wc.generate_from_frequencies(word_counts)

        image_path = f'static/img/wordcloud_{user_id}.png'
        wordcloud_gen.to_image().save(image_path, format='PNG')

# 데이터베이스 연결 정보 설정
host = '52.78.176.120'
user = 'root'
password = 'encore'
port = 3306
db = 'gorogoro'
charset = 'utf8'

# 사용자 ID 목록, 마스크 이미지 경로 및 폰트 경로 설정
user_ids = ['jin.99', 'aaa', 'bbb']  # user_ids들은 disticnt 문
mask_image_path = '/home/oh/workspace/다운로드.png'
font_path = '/home/oh/workspace/Font/malgunbd.ttf'

# 모든 사용자 ID에 대한 워드클라우드 생성
for i in user_ids:
    generate_wordclouds(host, user, password, port, db, charset, i, mask_image_path, font_path)