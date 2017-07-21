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


# 文章

from app01 import models
class ArticleForm(Form):
    def __init__(self,val,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)
        self.val = val
        self.fields['category_id'].choices = models.Category.objects.filter(blog__user=self.val).values_list('nid','title').all()
        self.fields['tags'].choices = models.Tag.objects.filter(blog__user=self.val).values_list('nid','title').all()

        print(self.val)


    title = fields.CharField(max_length=64)

    summary = fields.CharField(max_length=128)

    article_type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=models.Article.type_choices)
    )
    category_id = fields.ChoiceField(
        widget=widgets.RadioSelect
    )
    tags = fields.MultipleChoiceField(
        widget=widgets.CheckboxSelectMultiple
    )



    content = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'i1'})
    )




    def clean_content(self):
        old = self.cleaned_data['content']
        from utils.xss import xss

        return xss(old)




