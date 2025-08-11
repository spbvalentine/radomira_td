from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import requests

from django.shortcuts import render

@login_required
def dashboard_index(request):
    return render(request, 'adminator/index.html')

@login_required
def dashboard_call(request):
    return render(request, 'adminator/call.html')

def dashboard_login(request):
    return render(request, 'adminator/login.html')

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_index')
        else:
            error = 'Неверный логин или пароль'
    return render(request, 'adminator/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('dashboard_login')

def dashboard_report(request):
    return render(request, 'adminator/reports.html')

API_ENDPOINT = "http://127.0.0.1:8000/api/calls/"

@login_required  # ← автоматически перенаправит на login, если не авторизован
def dashboard_calls(request):
    try:
        # Создаём сессию, чтобы передать куки (включая сессию и CSRF)
        session = requests.Session()

        # Копируем сессионную куку из Django (она уже есть в request)
        # Django автоматически устанавливает сессионную куку при входе
        if 'sessionid' in request.COOKIES:
            session.cookies.set('sessionid', request.COOKIES['sessionid'])
        if 'csrftoken' in request.COOKIES:
            session.cookies.set('csrftoken', request.COOKIES['csrftoken'])

        # Делаем GET-запрос к API — с теми же куками, что и у пользователя
        response = session.get(API_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        calls = data['results']

    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("Status code:", e.response.status_code)
            print("Response:", e.response.text)
        calls = []

    return render(request, 'adminator/calls.html', {'calls': calls})

@login_required
def call_edit(request, call_id):
    return render(request, 'adminator/call_edit.html', {'call_id': call_id})