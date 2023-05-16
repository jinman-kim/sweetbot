from django.shortcuts import render
from django.db import connection
from collections import Counter
from wordcloud import WordCloud
# Create your views here.

def keywords(request):
    
    return render(request, 'keywords/key_main.html')



def generate_wordcloud(text):
    # 텍스트를 전처리하고 단어 빈도수를 계산하는 작업 수행
    # ...

    wc = WordCloud(font_path='/path/to/font.ttf', width=400, height=400, scale=2.0, max_font_size=250)
    frequencies = Counter(words)
    wc.generate_from_frequencies(frequencies)

    return wc.to_image()

def wordcloud_view(request):
    # 데이터베이스에서 텍스트 데이터 조회
    with connection.cursor() as cursor:
        cursor.execute("SELECT text_field FROM your_table")
        results = cursor.fetchall()
    
    texts = [result[0] for result in results]

    # 텍스트 데이터를 합침 (예: 리스트의 문자열을 하나의 문자열로)
    combined_text = ' '.join(texts)

    # 워드클라우드 생성
    image = generate_wordcloud(combined_text)

    # 웹페이지에 워드클라우드 이미지와 기타 정보 전달
    context = {
        'wordcloud_image': image,
        # 추가적인 정보를 필요에 따라 전달할 수 있습니다.
    }

    return render(request, 'wordcloud.html', context)