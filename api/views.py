import google.generativeai as genai
import requests
from django.http import JsonResponse

from api.api_lib.youtube_api import search_yt


def get_response(user_input, api_key):
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are Dev Rex, a programmer that helps students to learn."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.exceptions.HTTPError as http_err:
        print('HTTP error occurred:', http_err)
        return {'error': 'Request not successful'}
    except requests.exceptions.RequestException as req_err:
        print('Request error occurred:', req_err)
        return {'error': 'Request not successful'}


def perplexity_ai(request, api_key, prompt):
    response_data = get_response(prompt, api_key)
    if 'error' in response_data:
        return JsonResponse({'error': response_data['error']})
    else:
        response_message = response_data['choices'][0]['message']['content']
        return JsonResponse({'response': response_message})


def gemini_ai(request, api_key, prompt):
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 4096,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    try:
        convo = model.start_chat(history=[])

        convo.send_message(prompt)
        response = convo.last.text

        return JsonResponse({"response": response})
    except Exception as e:
        print("Error : ", str(e))
        error_message = "Prompt is unacceptable, Please try again!"
        return JsonResponse({"response": error_message})


def youtube_music_downloader(request, yt_key, cloud_name, cloud_key, secret_key, search_prompt):
    result = search_yt(search_prompt, yt_key, cloud_name, cloud_key, secret_key)
    return JsonResponse(result)
