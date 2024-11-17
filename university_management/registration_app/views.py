from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Student
import requests
from langchain_core.prompts import PromptTemplate
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login as login_hug
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


# login_hug("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")

# # Cargar el modelo y el tokenizador
# model_name = "meta-llama/Llama-3.1-405B"
# pipe = pipeline("text-generation", model=model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)


# def generate_response(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     outputs = model.generate(**inputs)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response


# def query_llama(request):
#     if request.method == "POST":
#         prompt = request.POST['prompt']
#         response = generate_response(prompt)
#         return JsonResponse({'response': response})
#
#     return render(request, 'templates/query_llama.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


def chat_view(request):
    if request.method == 'POST':
        # Get the message from the POST request
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

            if not message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # You can process the message here (e.g., use a chatbot API like OpenAI or a custom response)
            response_message = f"Received your message: {message}"

            return JsonResponse({'response': response_message})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
