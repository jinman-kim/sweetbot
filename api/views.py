from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import timedelta
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import openai
import threading
import time
import os, environ
import uuid
# from decouple import config
# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )
# # reading .env file
# environ.Env.read_env()


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


openai.api_key = os.environ.get('OPENAI_API_KEY')



def generate_response(request, session_messages, temperature):
    try:
        user_input = session_messages[-1]['content']  # 사용자의 입력 가져오기
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='\n'.join([f'{m["role"]}: {m["content"]}' for m in session_messages[:-1]]),  # 마지막 입력 제외
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=temperature,
            frequency_penalty=0,
            presence_penalty=0,
        )

        generated_text = response.choices[0].text.strip()
        if 'chatbot:' in generated_text:
            response_text = generated_text.split('chatbot:')[1].strip()
        elif 'chat:' in generated_text:
            response_text = generated_text.split('chat:')[1].strip()
        else:
            response_text = generated_text

        request.session['messages'].append(
            {"role": "chat", "content": response_text, "id": str(uuid.uuid4())})
        print('Generated response:', response_text)

    except Exception as e:
        print(f"Failed to generate response: {e}")
        request.session['messages'].append(
            {"role": "chat", "content": "Sorry, I could not generate a response at this time."})
    
    request.session.modified = True


    

def home(request):
    try:
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "chat", "content": f"지금부터 너는 연애 챗봇 친구야"},
            ]
        
        if request.method == 'POST':
            prompt = request.POST.get('prompt')  # prompt 가져오기
            temperature = float(request.POST.get('temperature', 0.1))
            
            request.session['messages'].append({"role": "user", "content": prompt})
            request.session.modified = True
            
            generate_response(request, request.session['messages'], temperature)  # 답변 생성
            
            max_messages = 10  # 유지할 최대 메시지 수
            if len(request.session['messages']) > max_messages:
                request.session['messages'] = request.session['messages'][-max_messages:]
            
            # 메시지 렌더링을 위한 처리
            displayed_messages = [
                message for message in request.session['messages'] if message.get('display', True)
            ]
            context = {
                'messages': displayed_messages,
                'prompt': '',
                'temperature': 0.1,
            }
            
            return render(request, 'home_test1.html', context)
        
        else:
            if hasattr(request, 'formatted_response'):
                formatted_response = request.formatted_response
                print("formatted_response:", formatted_response)
                request.session['messages'].append({"role": "user", "content": prompt, "display": False})
                del request.formatted_response
                request.session.modified = True

            # 메시지 렌더링을 위한 처리
            displayed_messages = [
                message for message in request.session['messages'] if message.get('display', True)
            ]
            context = {
                'messages': displayed_messages,
                'prompt': '',
                'temperature': 0.1,
            }

            return render(request, 'home_test1.html', context)
    except Exception as e:
        print(e)
        return redirect('error_handler')



def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('home')


# this is the view for handling errors
def error_handler(request):
    return render(request, '404.html')



def choose_mbti(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        return redirect('mbti_chatbot', prompt=prompt)
    return render(request, 'choose_mbti.html')



def mbti_chatbot(request, prompt):
    try:
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "chat", "content": "지금부터 너는 연애 챗봇 친구야"},
            ]

        if request.method == 'POST':
            prompt = request.POST.get('prompt')  # 사용자가 입력한 prompt 값 가져오기
            temperature = float(request.POST.get('temperature', 0.1))

            if 'prompt' not in request.session:
                request.session['messages'].append({
                    "role": "user",
                    "content": f"너는 MBTI가 {prompt}이야."
                })

            request.session['prompt'] = prompt

            request.session['messages'].append({"role": "user", "content": prompt})
            request.session.modified = True

            generate_response(request, request.session['messages'], temperature)  # 답변 생성

            max_messages = 10
            if len(request.session['messages']) > max_messages:
                request.session['messages'] = request.session['messages'][-max_messages:]

            displayed_messages = [
                message for message in request.session['messages'] if message.get('display', True)
            ]
            context = {
                'messages': displayed_messages,
                'prompt': '',
                'temperature': 0.1,
            }

            return render(request, 'mbti_chatbot.html', context)

        else:
            if hasattr(request, 'formatted_response'):
                formatted_response = request.formatted_response
                print("formatted_response:", {formatted_response})
                request.session['messages'].append({"role": "user", "content": formatted_response})
                del request.formatted_response
                request.session.modified = True

            displayed_messages = [
                message for message in request.session['messages'] if message.get('display', True)
            ]
            context = {
                'messages': displayed_messages,
                'prompt': '',
                'temperature': 0.1,
            }

            return render(request, 'mbti_chatbot.html', context)

    except Exception as e:
        print(e)
        return redirect('error_handler')
