from django import forms
from .models import Gender, User
from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)

class SigninForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="パスワード再入力", widget=forms.PasswordInput)
    username = forms.CharField(label="ユーザー名")
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(), # DBデータの取得
        widget=forms.Select,
        empty_label="選択してください",
        label="性別"
    )
    barrier_free = forms.BooleanField(
        required=False,
        label="バリアフリー優先",
    )

    class Meta:
        model = User
        fields = ("email", "password", "username", "gender", "barrier_free")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        print('password', password)
        confirm_password = cleaned_data.get("confirm_password")
        print(confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("パスワードが一致しません。")

        print("clean処理は完了しました")
        return cleaned_data

    def save(self):
        # user = super().save(commit=False)
        print("saveメソッドが呼ばれました")
        user = User(
            email=self.cleaned_data.get("email"),
            username=self.cleaned_data.get("username"),
            gender_id=self.cleaned_data.get("gender").id,
            is_barrier_free=self.cleaned_data.get("barrier_free"),
        )
        validate_password(self.cleaned_data.get("password"), user)
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user
