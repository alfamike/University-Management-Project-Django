from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Student
import requests
from .services import register_student_in_fabric, get_student_record_from_fabric
from langchain_core.prompts import PromptTemplate
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login as login_hug
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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


def register_student(request):
    if request.method == "POST":
        student_id = request.POST['student_id']
        name = request.POST['name']
        grade = request.POST['grade']

        # Lógica para registrar al estudiante en Hyperledger Fabric
        # Aquí llamarías a tu API de Hyperledger Fabric para registrar al estudiante
        register_student_in_fabric(student_id, name, grade)
        return redirect('student_list')

    return render(request, 'registration_app/register_student.html')


def student_list(request):
    students = Student.objects.all()
    return render(request, 'registration_app/student_list.html', {'students': students})


def get_student_record(request, student_id):
    # Lógica para obtener el registro del estudiante desde Hyperledger Fabric
    # Aquí llamarías a tu API de Hyperledger Fabric para obtener el registro del estudiante
    student_record = get_student_record_from_fabric(student_id)
    return JsonResponse(student_record)

    # response = {
    #     'student_id': student_id,
    #     'name': 'Nombre de prueba',
    #     'grade': 'A',
    #     # Otros datos que obtengas de Hyperledger
    # }
    # return JsonResponse(response)


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
