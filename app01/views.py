from django.shortcuts import render,redirect,HttpResponse

from app01 import models
from utils.pager import PageInfo

from app01.forms import LoginForm
from app01.forms import RegisterForm

def auth(func):
    def wrapper(request,*args,**kwargs):
        user = request.session.get('username')
        if user :
            v = func(request,*args,**kwargs)
            return v
        else:
            return redirect('/login.html')
    return wrapper



def index(request,*args,**kwargs):

    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    condition = {}
    all_count = models.Article.objects.all().count()
    if type_id:
        condition['article_type_id'] = type_id
        all_count = models.Article.objects.filter(**condition).count()

    page_info = PageInfo(request.GET.get('page'), all_count, 6,str(request.path_info))
    article_list = models.Article.objects.filter(**condition)[page_info.start:page_info.end]

    # 如果少于一页不显现分页
    if all_count <= 6:
        page_info = None

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
        file_path = os.path.join('static/img/avatar',file_obj.name)
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


        status = False
        if request.session.get('username'):
            login_obj = models.UserInfo.objects.filter(username=request.session.get('username')).first()
            if login_obj.username == user_obj.username:
                status = True



        else:
            login_obj = None

        article_list = models.Article.objects.filter(blog__user__username=username)
        focus_obj = models.UserFans.objects.filter(follower__username=username)

        if kwargs.get('tag'):
            tag = kwargs['tag']
            print(tag)
            article_list = models.Article.objects.filter(blog__user__username=username,tags=tag)
        if kwargs.get('category'):
            category = kwargs['category']
            article_list = models.Article.objects.filter(blog__user__username=username,category=category)

        all_count = article_list.count()
        page_info = PageInfo(request.GET.get('page'), all_count, 6, str(request.path_info))
        article_list = article_list[page_info.start:page_info.end]

        # 如果少于一页不显现分页
        if all_count <= 6:
            page_info = None


        from django.db.models import Count

        a2t_list = models.Article2Tag.objects.filter(tag__blog__site=site).values('tag__title','tag__nid').annotate(aa = Count('tag__title'))
        # print(a2t_list.query)

        category_list = models.Article.objects.filter(blog__site=site).values('category__title','category__nid').annotate(aa = Count('category__title'))
        # print(category_list.query)


        # mysql 数据库写法
        # data_list = models.Article2Tag.objects.filter(blog__site=site).extra(select={'c':"date_format(create_time,'%%Y-%%m')"}).values('c').annotate(ct=Count('nid'))



        return render(request, 'UserBlog.html', {'blog_obj':blog_obj,
                                                 'user_obj':user_obj,
                                                 'login_obj':login_obj,
                                                 'article_list':article_list,
                                                 'focus_obj':focus_obj,
                                                 'status': status,
                                                 'page_info': page_info,

                                                 'a2t_list':a2t_list,
                                                 'category_list':category_list
                                                 })
    else:
        return redirect('/index.html')




