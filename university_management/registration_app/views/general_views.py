import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render


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
    """
    Render the login page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered HTML response for the login page.
    """
    return render(request, 'registration/login.html')


def logout(request):
    """
    Handle user logout by deleting the authentication cookie and redirecting to the login page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A redirect response to the login page.
    """
    response = redirect('login')
    response.delete_cookie('auth_token')
    return response


def home(request):
    """
    Render the home page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: A rendered HTML response for the home page.
    """
    return render(request, 'home.html')


def chat_view(request):
    """
    Handle chat messages sent via POST request and return a response.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the chat response or an error message.
    """
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
