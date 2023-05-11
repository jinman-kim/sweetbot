from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import timedelta
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import openai
import threading
import time
import os, environ

from decouple import config

# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )
# # reading .env file
# environ.Env.read_env()

# OPENAI_KEY = env('OPENAI_KEY')
openai.api_key = config('OPENAI_API_KEY')


def generate_response(request, session_messages, temperature):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt='\n'.join([f'{m["role"]}: {m["content"]}' for m in session_messages]),
        temperature=temperature,
        max_tokens=1000,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
    )
    print(response.choices[0].text)
    request.session['messages'].append({"role": "chat", "content": response.choices[0].text.strip()})

def generate_response(request, session_messages, temperature):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt='\n'.join([f'{m["role"]}: {m["content"]}' for m in session_messages]),
            temperature=temperature,
            max_tokens=1000,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0,
        )
        print(response.choices[0].text)
        request.session['messages'].append({"role": "chat", "content": response.choices[0].text.strip()})
    except Exception as e:
        print(f"Failed to generate response: {e}")
        request.session['messages'].append({"role": "chat", "content": "Sorry, I could not generate a response at this time."})
    request.session.modified = True

def home(request):
    try:
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "지금부터 너는 내 애인이야.."},
            ]
        if request.method == 'POST':
            prompt = request.POST.get('prompt')
            temperature = float(request.POST.get('temperature', 0.1))
            request.session['messages'].append({"role": "user", "content": prompt})
            request.session.modified = True

            # generate response in a separate thread
            response_thread = threading.Thread(target=generate_response, args=(request, request.session['messages'], temperature))
            response_thread.start()
            response_thread.join(timeout=60)

            context = {
                        'messages': request.session['messages'],
                        'prompt':'',
                        'temperature': temperature,
                    }
            return render(request, 'home.html', context)
        
        else:
            if hasattr(request, 'formatted_response'):
                formatted_response = request.formatted_response
                print(formatted_response)
                request.session['messages'].append({"role": "chat", "content": formatted_response})
                del request.formatted_response
                request.session.modified = True

            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'home.html', context)
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