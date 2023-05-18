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
from api.models import Feed
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from chat.settings import MEDIA_ROOT


# from decouple import config
# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )
# # reading .env file
# environ.Env.read_env()


#env = environ.Env(
#    # set casting, default value
#    DEBUG=(bool, False)
#)

# Set the project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
#environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


openai.api_key = 'SECRET_KEY'

def index(request):
    return render(request, 'index.html')


def generate_response(request, session_messages, temperature):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='\n'.join([f'{m["role"]}: {m["content"]}' for m in session_messages]),
            # prompt='\n'.join([f'{}'])
            max_tokens=1000,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0,
        )
        # uuid : 답변의 id를 줌으로써 텍스트가 중복되어 나오는 경우 차단

        print('test_response:', response.choices[0].text, len(response.choices[0].text))
        if 'chatbot:' in response.choices[0].text.strip():
            request.session['messages'].append(
                {"role": "chat", "content": response.choices[0].text.strip().split('chatbot:')[1], "id": str(uuid.uuid4())})
            print('chatbot removed')
        elif 'chat:' in response.choices[0].text.strip():
            request.session['messages'].append(
                {"role": "chat", "content": response.choices[0].text.strip().split('chat:')[1], "id": str(uuid.uuid4())})
            print('chat removed')

        else:
            request.session['messages'].append(
                {"role": "chat", "content": response.choices[0].text.strip(),
                 "id": str(uuid.uuid4())})
        print('test:',request.session['messages'][-1]['content'])
    except Exception as e:
        print(f"Failed to generate response: {e}")
        request.session['messages'].append(
            {"role": "chat", "content": "Sorry, I could not generate a response at this time."})
    request.session.modified = True


def home(request):
    try:
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "chat", "content": f"지금부터 너는 내 개발 도우미야"},
            ]
        # 포스트 요청이 들어올 때 ( 사용자가 채팅 전송을 할 때 )
        if request.method == 'POST':
            prompt = request.POST.get('prompt')
            temperature = float(request.POST.get('temperature', 0.1))
            request.session['messages'].append({"role": "user", "content": prompt})
            request.session.modified = True

            # generate response in a separate thread
            response_thread = threading.Thread(target
                                               =generate_response,
                                               args
                                               =(request, request.session['messages'], temperature))
            response_thread.start()
            response_thread.join(timeout=60)

            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'chat/home.html', context)

        # GET 요청 들어올 때,
        else:
            # request 가 formatted_response를 갖고 있다면,
            if hasattr(request, 'formatted_response'):
                formatted_response = request.formatted_response
                print("formatted_response:", {formatted_response})
                request.session['messages'].append({"role": "user", "content": formatted_response})
                del request.formatted_response
                request.session.modified = True

            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'chat/home.html', context)
    except Exception as e:
        print(e)
        return redirect('error_handler')


def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('chat/home.html')


# this is the view for handling errors
def error_handler(request):
    return render(request, 'index/404.html')


