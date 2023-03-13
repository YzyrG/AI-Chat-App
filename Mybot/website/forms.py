from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# 集成自定义用户模型到后台管理界面
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}), help_text='<span class="form-text text-muted"><small>必填；请输入正确的邮件格式。</small></span>')

    class Meta:
        model = User
        fields = ('username', 'email',  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        # 使用super继承父类UserCreationForm的构造函数__init__()
        super().__init__(*args, **kwargs)

        # 自定义表单html属性
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted">' \
                                            '<small>必填；长度为150个字符或以下；只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”。</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small">' \
                                             '<li><small>您的密码不能与您的其他个人信息过于相似。</small></li>' \
                                             '<li><small>您的密码必须至少包含 8 个字符。</small></li>' \
                                             '<li><small>您的密码不能是常用密码。</small></li>' \
                                             '<li><small>您的密码不能完全是数字。</small></li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>请再次输入以确认密码。</small></span>'
