from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .models import User
from . import forms

def home(request):
    return render(request, 'accounts/home.html')

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

@login_required
def user_logout(request):
    logout(request)
    # messages.success(request, 'ログアウトしました')
    return render(request, 'accounts/user_logout.html')

def password_reset_request(request):
    """パスワードリセットリクエスト（メール送信）"""
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            print('email', email)

            try:
                user = User.objects.get(email=email)
                print("取得したuserID:", user.pk, str(user.pk))
                uid = urlsafe_base64_encode(str(user.pk).encode())
                print('uid', uid)
                token = default_token_generator.make_token(user)
                print('token', token)

                # フルパスのURL作成
                reset_url = request.build_absolute_uri(reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
                print('reset_url', reset_url)

                # メールのレンダリング
                subject = render_to_string('accounts/password_reset/subject.txt', {"user": user})
                message = render_to_string('accounts/password_reset/message.txt', {"reset_url": reset_url, "user":user})

                send_mail(subject, message, None, [user.email])
                # message.success(request, "パスワードリセットのメールを送信しました。")
                print("パスワードリセットのメールを送信しました。")

                return redirect("accounts:password_reset_done")

            except User.DoesNotExist:
                print("該当するユーザーが見つかりません")

    else:
        form = PasswordResetForm()

    return render(request, 'accounts/password_reset/password_reset_form.html', {"form": form})

def password_reset_done(request):
    """パスワードリセットメール送信完了ページ"""
    return render(request, 'accounts/password_reset/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    """新しいパスワード設定ページ"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print('password_reset_confirmのuid', uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) :
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # messages.success(request, "パスワードが変更されました。")
                # print("パスワードが変更されました。")
                return redirect("accounts:password_reset_complete")
        else:
            form = SetPasswordForm(user)

        return render(request, "accounts/password_reset/password_reset_confirm.html", {"form": form})
    
    else:
        # messages.error(request, "リンクが無効または期限切れです。")
        print("リンクが無効または期限切れです。")
        return redirect("accounts:password_reset_request")
    
def password_reset_complete(request):
    """パスワードリセット完了ページ"""
    return render(request, "accounts/password_reset/password_reset_complete.html")