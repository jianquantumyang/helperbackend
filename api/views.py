from django.shortcuts import render
from openai import OpenAI
from backendhelper.settings import OPENAI_API_KEY,MEDIA_ROOT
import os
from django.views.decorators.csrf import csrf_exempt 
import json
from django.http.response import JsonResponse
import uuid

opnai = OpenAI(api_key=OPENAI_API_KEY)

@csrf_exempt
def index(request):
    return JsonResponse({"message":"hello!"})


@csrf_exempt
#text to text
def chattxt(request):
    if request.method=="POST":
        data = json.loads(request.body)
        message = data.get('message')

        response = opnai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system","content":"You are a helpful assistant that specializes in solving various PC problems. Your expertise includes handling text, directories, code, office applications, word processing, and more."},
                {"role": "user","content": message}
            ]
        )
        res = str(response.choices[0].message.content)
        #print(res)
        return JsonResponse({"answer": res})

    return JsonResponse({"error": "🤷‍♂️"}, status=405)

@csrf_exempt
#speech to text
def chatstt(request):
    if request.method=="POST" and 'audio' in request.FILES:

        audio_file = request.FILES['audio']    

        save_path = os.path.join(MEDIA_ROOT,f'{uuid.uuid4()}.wav')
        with open(save_path,'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)


        
        audio_fl = open(save_path,"rb")
        transcript = opnai.audio.transcriptions.create(
            model = "whisper-1", 
            file = audio_fl, 
            response_format="text"
        )
        audio_fl.close()
        response = opnai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system","content":"You are a helpful assistant that specializes in solving various PC problems. Your expertise includes handling text, directories, code, office applications, word processing, and more."},
                {"role": "user","content": transcript}
            ]
        )
        
        res = str(response.choices[0].message.content)

        if os.path.exists(save_path):
            os.remove(save_path)

        return JsonResponse({"answer": res})



    return JsonResponse({"error": "🤷‍♂️🤷‍♀️"}, status=405)



