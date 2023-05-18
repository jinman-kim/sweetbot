from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import os
import pymysql

try:
    con = pymysql.connect(host='52.78.176.120', user='root', password='encore',  
                          port=3306, db='gorogoro', charset='utf8')
    cur = con.cursor()
except Exception as e:
    print (e)


cur.execute("SELECT * FROM api_feed where user_id='jin.99'")
rows = cur.fetchall()
a = ' '.join([i[1] for i in rows]).replace(",", " ")

im = Image.open('/home/oh/workspace/다운로드.png')
mask_arr = np.array(im)

okt = Okt()
nouns = okt.nouns(a) # 명사만 추출

words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함

wc = WordCloud(font_path='/home/oh/workspace/Font/malgunbd.ttf', width=400,mask = mask_arr, height=400, scale=2.0, max_font_size=250,
               background_color ='#F7F7F7')
gen = wc.generate_from_frequencies(c)

image_path = os.path.join('static/img/', 'wordcloud.png')
gen.to_image().save(image_path, format='PNG')