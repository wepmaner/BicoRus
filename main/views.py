from django.shortcuts import render, HttpResponse, HttpResponseRedirect,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.

def index_view(request):
    return render(request, 'main/index.html')

def contacts_view(request):
    return render(request, 'main/contacts.html')

def login_view(request):
    if request.method == 'POST':
        auth_form = LoginForm(request.POST)
        if auth_form.is_valid():
            login_user = auth_form.cleaned_data['Login']
            password = auth_form.cleaned_data['Password']
            user = authenticate(request, username=login_user, password=password)   
            if user is not None:
                if hasattr(user, 'usertotp'):
                    request.session['otp_user_id'] = user.id
                    return redirect('login/2fa')
                else:
                    login(request, user)
                    return redirect(request.GET.get('next','/'))
            else:
                auth_form.add_error(None, 'Неправильный логин или пароль')
    else:
        auth_form = LoginForm()
    return render(request, 'main/login.html', {
        'auth_form': auth_form,
    })

def login_2fa_view(request):
    if request.method == 'POST':
        totp_form = TOTPConfirmForm(request.POST) 
        if totp_form.is_valid():
            #получаем id пользователя и введеный код
            user_id = request.session['otp_user_id']
            totp_code = totp_form.cleaned_data['Code']
            user = User.objects.get(id=user_id)
            totp = pyotp.TOTP(user.usertotp.secret_key)
            if totp.verify(totp_code):
                login(request, user)
                return redirect('/')
            else:
                totp_form.add_error(None,'Неправильный код')
    else:
        totp_form = TOTPConfirmForm()
    return render(request, 'main/2fa.html', {
        'totp_form': totp_form
    })

def registration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login_user = form.cleaned_data['Login']
            password = form.cleaned_data['Password']
            confirm_password = form.cleaned_data['ConfirmPassword']
            if User.objects.filter(username=login_user).exists():
                form.add_error(None, 'Пользователь с таким логином уже существует')
            else:
                if password == confirm_password:
                    user_info = User.objects.create_user(username=login_user, password=password)
                    user_info.save()
                    user = authenticate(request, username=login_user, password=password)
                    login(request, user)
                    redirect('/')
                else:
                    form.add_error(None, 'Пароли не совпаают')
        else:
            form.add_error(None, 'Что-то пошло не так')

            
    else:
        form = RegisterForm()
    return render(request, 'main/registration.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    path = reverse('home')
    return HttpResponseRedirect(path)



#---------------------------------------------------------
from .utils import *
def polygon_view(request):
    form = DocumentForm()
    documents = Document.objects.all()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = request.user

            post_instance = Post.objects.get(id=1)
            document.post = post_instance 
            document.save()
        totp_form = TOTPConfirmForm(request.POST)
        if totp_form.is_valid():
            
            code = totp_form.cleaned_data['Code']
            print(code)
    
    return render(request, 'main/polygon.html', {
        'form': form,
        'documents': documents
    })

def polygon2_view(request):
    if request.method == 'POST':
        form = TOTPConfirmForm(request.POST)

    return render(request, 'main/polygon2.html', {
    })

@login_required
def otp_settings_view(request):
    success = False
    otp = {
        'file_url':request.session.get('file_url',''),
        'secret_key':request.session.get('otp_secret_key','')
        }
    form = TOTPConfirmForm()
    if request.method == 'POST':
        form = TOTPConfirmForm(request.POST)
        if form.is_valid():
            Code = form.cleaned_data['Code']
            if otp_verify(request,Code):
                success = True
                usertotp = UserTotp(user=request.user, secret_key=otp['secret_key'])
                usertotp.save()
                del request.session['otp_secret_key']
            else:
                form.add_error(None, 'Неправильный код')
                success = False
        else:
            form.add_error(None, 'Неизвестная ошибка')
        
    elif hasattr(request.user, 'usertotp'):
            success = True
    else:
        success = False
        otp_send(request)

    return render(request, 'main/otp-settings.html', {
        'success': success,
        'otp': otp,
        'form': form
    })