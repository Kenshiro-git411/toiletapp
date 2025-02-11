from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ValidationError
from . import forms

def user_login(request):
    login_form = forms.LoginForm()

    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'ログインしました。')
                print('ログインしました')
                return redirect('accounts:home')
            else:
                messages.warning(request, 'メールアドレスかパスワードが間違っています。')

    return render(request, 'accounts/user_login.html', context={
        'login_form': login_form,
    })

def user_create(request):
    signin_form = forms.SigninForm()

    if request.method == 'POST':
        print("POSTデータ", request.POST)
        signin_form = forms.SigninForm(request.POST)

        if signin_form.is_valid():
            print("ここまで来てる")

            try:
                signin_form.save()
                return redirect('accounts:home')
            except ValidationError as e:
                signin_form.add_error('password', e)
                print(type(e).__name__, e)
        else:
            print("ValidationError:", signin_form.errors)

    return render(request, 'accounts/user_create.html', context={
        'signin_form': signin_form,
    })



