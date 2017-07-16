from django.forms import Form
from django.forms import fields
from django.forms import widgets




class LoginForm(Form):
    """
    登陆页面的Form验证
    """
    username = fields.CharField(
        required=True,
        error_messages={
            'required': '用户名不能为空!'
        },
        widget = widgets.TextInput(attrs={'class': 'form-control','placeholder':'user','name':'username'})

    )

    password = fields.CharField(
        required=True,
        error_messages={
            'required': '密码不能为空!'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'name': 'password'})
    )
    code = fields.CharField(
        required=True,
        min_length=5,
        max_length=5,
        error_messages={
            'required': '验证码不能为空!',
            'min_length': '验证码为5位!',
            'max_length': '验证码为5位!',

        },
        widget = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'code', 'name': 'code'})

    )




class RegisterForm(Form):
    """
    注册页面的Form验证
    """
    username = fields.CharField(
        max_length=32,
        min_length=4,
        required=True,
        error_messages={
            'max_length': '用户名太长！',
            'min_length':'用户名太短！',
            'required': '用户名不能为空!',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'user', 'name': 'username'})
    )

    nickname = fields.CharField(
        max_length=32,
        min_length=4,
        required=True,
        error_messages={
            'max_length': '昵称太长！',
            'min_length':'昵称太短！',
            'required': '昵称不能为空!',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'nickname', 'name': 'nickname'})
    )

    email = fields.EmailField(
        required=True,
        error_messages={
            'required': '用户名不能为空!',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'email', 'name': 'email'})
    )

    password = fields.CharField(
        max_length=64,
        min_length=6,
        required=True,
        error_messages={
            'max_length': '密码太长！',
            'min_length': '密码太短！',
            'required': '密码不能为空!'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'name': 'password'})
    )
    password02 = fields.CharField(
        max_length=64,
        min_length=6,
        required=True,
        error_messages={
            'max_length': '密码太长！',
            'min_length': '密码太短！',
            'required': '密码不能为空!'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次确认', 'name': 'password02'})
    )
    code = fields.CharField(
        required=True,
        min_length=5,
        max_length=5,
        error_messages={
            'required': '验证码不能为空!',
            'min_length': '验证码为5位!',
            'max_length': '验证码为5位!',

        },
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'code', 'name': 'code'})

    )




