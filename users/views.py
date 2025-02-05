from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


def home(request):
    return render(request, 'users/home.html')


def registrar(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'oi {username}, sua conta foi criada com sucesso')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/registrar.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'users/profile.html')

@csrf_exempt
@login_required()
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Recebe a mensagem do usuário
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"error": "Mensagem vazia"}, status=400)

            # Criar modelo e gerar resposta
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(user_message)

            return JsonResponse({"response": response.text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "users/chatbot.html")

def sobre(request):
    return render(request, 'users/sobre.html')

def logout(request):
    return render(request, 'users/logout.html')

