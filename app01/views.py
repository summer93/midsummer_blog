from django.shortcuts import render,redirect,HttpResponse

from app01 import models
from utils.pager import PageInfo


def auth(func):
    def wrapper(request,*args,**kwargs):
        user = request.session.get('username')
        if user :
            v = func(request,*args,**kwargs)
            return v
        else:
            return redirect('/login.html')
    return wrapper

from django.forms import Form
from django.forms import fields
from django.forms import widgets
class LoginForm(Form):
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



def index(request,*args,**kwargs):

    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    condition = {}
    all_count = models.Article.objects.all().count()
    if type_id:
        condition['article_type_id'] = type_id
        all_count = models.Article.objects.filter(**condition).count()
    c =request.path_info
    print(c)
    page_info = PageInfo(request.GET.get('page'), all_count, 6,str(request.path_info))
    article_list = models.Article.objects.filter(**condition)[page_info.start:page_info.end]

    type_choicesList = models.Article.type_choices
    if request.session.get('username'):
        user_obj = models.UserInfo.objects.filter(username=request.session.get('username')).first()

    else:
        user_obj = None

    # user_list = models.Article.objects.all()[page_info.start:page_info.end]
    # return render(request, 'index.html', {'user_list': user_list, 'page_info': page_info, 'sex': sex})

    return render(request,'index.html',{'type_choices_list':type_choicesList,'article_list':article_list,'type_id':type_id,'page_info': page_info,'user_obj':user_obj})

def check_code(request):

    from io import BytesIO
    from utils.random_check_code import rd_check_code
    img,code = rd_check_code()
    stream = BytesIO()
    img.save(stream,'png')
    request.session['code'] = code

    return HttpResponse(stream.getvalue())


def login(request):

    if request.method == 'GET':
        obj = LoginForm()
        return render(request,'login.html',{'obj':obj})
    else:
        obj = LoginForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        log_time = request.POST.get('log_time')

        if obj.is_valid():
            print(obj.cleaned_data)


            if code.upper() == request.session.get('code').upper():
                user_obj = models.UserInfo.objects.filter(username=username, password=password).first()
                if user_obj:
                    print(user_obj.username)
                    request.session['username'] = username
                    print('ok')
                    print(log_time)
                    # 设置过期时间
                    if log_time:
                        request.session.set_expiry(int(log_time))
                    return redirect('/index.html')
                else:
                    return render(request, 'login.html',{'errormsg':'用户名或密码错误！','obj':obj})
            else:
                return render(request,'login.html',{'codemsg':'验证码错误！','obj':obj})
        else:
            return render(request,'login.html',{'obj':obj})

def logout(request):
    request.session.delete()
    return redirect('/index.html')



class RegisterForm(Form):
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







def register(request):
    if request.method == 'GET':
        obj = RegisterForm()
        return render(request,'register.html',{'obj':obj})
    else:

        obj = RegisterForm(request.POST)

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password02 = request.POST.get('password02')
        code = request.POST.get('code')
        if password != password02:
            return render(request,'register.html',{'errormsg':'两次密码不一致！','obj':obj})
        if obj.is_valid():
            if code.upper() == request.session.get('code').upper():
                obj.cleaned_data.pop('password02')
                obj.cleaned_data.pop('code')
                obj.cleaned_data['avatar'] = "/"+request.session.get('avatar')
                models.UserInfo.objects.create(**obj.cleaned_data)
                return redirect('/login.html')
            else:
                return render(request, 'register.html', {'codemsg': '验证码错误！','obj':obj})
        else:
            return render(request, 'register.html', {'obj': obj})




def upload(request):
        file_obj = request.FILES.get('HeadPicture')
        import os
        file_path = os.path.join('static',file_obj.name)
        with open(file_path,'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        request.session['avatar'] = file_path
        return HttpResponse(file_path)






# 个人主页


def userblog(request,site,*args,**kwargs):
    """
    
    :param request: 
    :param site: url 传入的个人博客前缀
    :return: 
    """

    blog_obj = models.Blog.objects.filter(site=site).first()

    # user_obj = models.UserInfo.objects.filter(username=username).first()
    if blog_obj:
        user_obj = blog_obj.user
        username = user_obj.username

        article_list = models.Article.objects.filter(blog__user__username=username)
        focus_obj = models.UserFans.objects.filter(follower__username=username)

        if kwargs.get('tag'):
            tag = kwargs['tag']
            print(tag)
            article_list = models.Article.objects.filter(blog__user__username=username,tags=tag)
        if kwargs.get('category'):
            category = kwargs['category']
            article_list = models.Article.objects.filter(blog__user__username=username,category=category)






        from django.db.models import Count

        a2t_list = models.Article2Tag.objects.filter(tag__blog__site=site).values('tag__title','tag__nid').annotate(aa = Count('tag__title'))

        category_list = models.Article.objects.filter(blog__site=site).values('category__title','category__nid').annotate(aa = Count('category__title'))



        return render(request, 'UserBlog.html', {'blog_obj':blog_obj,
                                                 'user_obj':user_obj,
                                                 'article_list':article_list,
                                                 'focus_obj':focus_obj,

                                                 'a2t_list':a2t_list,
                                                 'category_list':category_list
                                                 })
    else:
        return redirect('/index.html')










