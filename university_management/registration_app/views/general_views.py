import json
import asyncio
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import traceback
from registration_app.services_fabric.services_fabric import FabricClientSingleton


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

def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    response = redirect('')
    response.delete_cookie('auth-token')
    return response


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


@csrf_exempt
def init_fabric(request):
    try:
        singleton = FabricClientSingleton.get_instance()

        return JsonResponse({
            'success': True,
            'message': 'Fabric client initialized correctly for user'}
        )

    except ValueError as e:
        return JsonResponse({
            'error': str(e),
            'message': 'Failed to initialize Fabric client or user.',
            'stack_trace': traceback.format_exc()
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'error': 'An unexpected error occurred.',
            'message': str(e),
            'stack_trace': traceback.format_exc()
        }, status=500)
