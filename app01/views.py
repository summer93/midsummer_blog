from django.shortcuts import render,redirect,HttpResponse

from app01 import models
from utils.pager import PageInfo

from app01.forms import LoginForm
from app01.forms import RegisterForm
from app01.forms import ArticleForm
import json

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

    """
    主页
    :param request: 
    :param args: 
    :param kwargs: 
    :return: 
    """

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
    up_down_list = models.UpDown.objects.filter(user__username=request.session.get('username'))

    return render(request,'index.html',{'type_choices_list':type_choicesList,
                                        'article_list':article_list,
                                        'type_id':type_id,
                                        'page_info': page_info,
                                        'user_obj':user_obj,
                                        'up_down_list': up_down_list,
                                        })






def check_code(request):
    """
    生成随机验证码
    :param request: 
    :return: 
    """

    from io import BytesIO
    from utils.random_check_code import rd_check_code
    img,code = rd_check_code()
    stream = BytesIO()
    img.save(stream,'png')
    request.session['code'] = code

    return HttpResponse(stream.getvalue())



def login(request):
    """
    登陆页
    :param request: 
    :return: 
    """

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
    """
    账户注销
    :param request: 
    :return: 
    """
    request.session.delete()
    return redirect('/index.html')




def register(request):
    """
    注册页面
    :param request: 
    :return: 
    """
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
    """
    头像处理
    :param request: 
    :return: 
    """
    file_obj = request.FILES.get('HeadPicture')
    import os
    file_path = os.path.join('static/img/avatar', file_obj.name)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    request.session['avatar'] = file_path
    return HttpResponse(file_path)




#################  个人主页  #################







def home(request,site):

    blog_obj = models.Blog.objects.filter(site=site).first()

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

        # data_list = models.Article2Tag.objects.filter(blog__site=site).extra(select={'ct':"date_format(create_time,'%%Y-%%m')"}).values('ct').annotate(aa=Count('nid'))
        date_list = models.Article.objects.filter(blog__site=site).extra(select={'ct': "date_format(create_time,'%%Y-%%m')"}).values('ct').annotate(aa=Count('nid'))

        return render(request, 'home.html', {'blog_obj': blog_obj,
                                             'user_obj': user_obj,
                                             'login_obj': login_obj,
                                             'article_list': article_list,


                                             'focus_obj': focus_obj,
                                             'status': status,
                                             'page_info': page_info,

                                             'a2t_list': a2t_list,
                                             'category_list': category_list,
                                             'data_list': date_list

                                             })

    else:
        return redirect('/index.html')




def filter(request,site,key,val):
    blog_obj = models.Blog.objects.filter(site=site).first()

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



        if key == 'tag':
            article_list = models.Article.objects.filter(blog=blog_obj,tags=val)
        if key == 'category':
            article_list = models.Article.objects.filter(blog=blog_obj,category=val)
        if key == 'date':
            article_list = models.Article.objects.filter(blog=blog_obj).extra(where=["date_format(create_time,'%%Y-%%m')=%s"],params=[val, ])



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

        # data_list = models.Article2Tag.objects.filter(blog__site=site).extra(select={'ct':"date_format(create_time,'%%Y-%%m')"}).values('ct').annotate(aa=Count('nid'))
        date_list = models.Article.objects.filter(blog__site=site).extra(select={'ct': "date_format(create_time,'%%Y-%%m')"}).values('ct').annotate(aa=Count('nid'))

        return render(request, 'home.html', {'blog_obj': blog_obj,
                                             'user_obj': user_obj,
                                             'login_obj': login_obj,
                                             'article_list': article_list,

                                             'focus_obj': focus_obj,
                                             'status': status,
                                             'page_info': page_info,

                                             'a2t_list': a2t_list,
                                             'category_list': category_list,
                                             'data_list': date_list

                                             })

    else:
        return redirect('/index.html')








def article(request,site,val):
    """
    文章最终页
    :param request: 
    :param site: 
    :param val: 
    :return: 
    """

    blog_obj = models.Blog.objects.filter(site=site).first()

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

        focus_obj = models.UserFans.objects.filter(follower__username=username)







        from django.db.models import Count

        a2t_list = models.Article2Tag.objects.filter(tag__blog__site=site).values('tag__title','tag__nid').annotate(aa = Count('tag__title'))
        # print(a2t_list.query)

        category_list = models.Article.objects.filter(blog__site=site).values('category__title','category__nid').annotate(aa = Count('category__title'))
        # print(category_list.query)

        # mysql 数据库写法

        # data_list = models.Article2Tag.objects.filter(blog__site=site).extra(select={'ct':"date_format(create_time,'%%Y-%%m')"}).values('ct').annotate(aa=Count('nid'))
        date_list = models.Article.objects.filter(blog__site=site).extra(select={'ct': "date_format(create_time,'%%Y-%%m')"}).values('ct').annotate(aa=Count('nid'))

        article_detail = models.ArticleDetail.objects.filter(article=val).first()


        # 评论

        comments_list = models.Comment.objects.filter(article=val).values('nid', 'content','create_time','article_id','user__username','reply_id')

        comments_list_dict = {}
        for item in comments_list:
            item['child'] = []
            comments_list_dict[item['nid']] = item

        result = []
        for item in comments_list:
            pid = item['reply_id']
            if pid:
                comments_list_dict[pid]['child'].append(item)
            else:
                result.append(item)

        from utils.comment import comment_tree
        comment_str = comment_tree(result)

        print(result)









        return render(request, 'article.html', {'blog_obj': blog_obj,
                                                 'user_obj': user_obj,
                                                 'login_obj': login_obj,


                                                 'focus_obj': focus_obj,
                                                 'status': status,


                                                 'a2t_list': a2t_list,
                                                 'category_list': category_list,
                                                 'data_list': date_list,
                                                 'articleDetail': article_detail,

                                                 'comment_str': comment_str,



                                             })

    else:
        return redirect('/index.html')




def up_down(request):
    ret = {'status': True, 'upCount': None,'downCount':None}

    from django.db.models import F
    user = request.session.get('username')
    if user:
        article_nid = request.POST.get('article_nid')
        select  = request.POST.get('select')
        user_nid = models.UserInfo.objects.filter(username=user).first().nid

        user_obj = models.UpDown.objects.filter(article=article_nid,user__username=user).first()
        try:
            attr = user_obj.up
        except:
            attr = None

        if select == 'up':


            if attr == True:
                models.Article.objects.filter(nid=article_nid).update(up_count=F('up_count') - 1)
                models.UpDown.objects.filter(article_id=article_nid, user_id=user_nid, up=True).delete()
            elif attr == None:
                models.Article.objects.filter(nid=article_nid).update(up_count=F('up_count') + 1)
                models.UpDown.objects.create(article_id=article_nid,user_id=user_nid,up=True )
            elif attr == False:
                models.Article.objects.filter(nid=article_nid).update(down_count=F('down_count') - 1)
                models.Article.objects.filter(nid=article_nid).update(up_count=F('up_count') + 1)
                models.UpDown.objects.filter(article_id=article_nid, user_id=user_nid).update(up=True)

        elif select == 'down':

            if attr == False:
                models.Article.objects.filter(nid=article_nid).update(down_count=F('down_count') - 1)
                models.UpDown.objects.filter(article_id=article_nid, user_id=user_nid, up=False).delete()
            elif attr == None:
                models.Article.objects.filter(nid=article_nid).update(down_count=F('down_count') + 1)
                models.UpDown.objects.create(article_id=article_nid,user_id=user_nid,up=False )
            elif attr == True:
                models.Article.objects.filter(nid=article_nid).update(down_count=F('down_count') + 1)
                models.Article.objects.filter(nid=article_nid).update(up_count=F('up_count') - 1)
                models.UpDown.objects.filter(article_id=article_nid, user_id=user_nid).update(up=False)


        else:
            pass

        ret['upCount'] = models.Article.objects.filter(nid=article_nid).first().up_count
        ret['downCount'] = models.Article.objects.filter(nid=article_nid).first().down_count
        print(ret)
        return HttpResponse(json.dumps(ret))

    else:
        ret['status'] = False

        return HttpResponse(json.dumps(ret))




#########################  个人 管理   ##################################


@auth
def manage(request):

    login_obj = models.UserInfo.objects.filter(username=request.session.get('username')).first()
    article_obj = models.Article.objects.filter(blog__user=login_obj)

    type_list = models.Article.type_choices

    category_list = models.Category.objects.filter(blog__user=login_obj)
    tag_list = models.Tag.objects.filter(blog__user=login_obj)



    kwargs = {'article_type_id':0,'category_id':0,'tags__nid':0}
    return render(request,'manage_article.html',{
        'login_obj': login_obj,
        'article_obj': article_obj,
        'type_list': type_list,
        'category_list':category_list,
        'tag_list': tag_list,
        'kwargs': kwargs,


    })


@auth
def manage_article(request,**kwargs):
    print(kwargs)
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v
    print(condition)


    login_obj = models.UserInfo.objects.filter(username=request.session.get('username')).first()
    article_obj = models.Article.objects.filter(blog__user=login_obj,**condition)

    type_list = models.Article.type_choices

    category_list = models.Category.objects.filter(blog__user=login_obj)
    tag_list = models.Tag.objects.filter(blog__user=login_obj)
    print(tag_list)
    print(kwargs)
    return render(request,'manage_article.html',{
        'login_obj': login_obj,
        'article_obj': article_obj,
        'type_list': type_list,
        'category_list':category_list,
        'tag_list': tag_list,
        'kwargs': kwargs,

    })


@auth
def manage_add(request):

    login_obj = models.UserInfo.objects.filter(username=request.session.get('username')).first()
    blog_obj = models.UserInfo.objects.filter(username=request.session.get('username')).first()
    print('z',blog_obj.nid)

    if request.method == 'GET':
        obj = ArticleForm(val=login_obj)

        return render(request, 'manage_add.html',{
            'login_obj': login_obj,
            'obj':obj,
        })



    else:
        obj = ArticleForm(login_obj,request.POST)

        if obj.is_valid():
            print('ok',obj.cleaned_data)
            obj.cleaned_data['read_count'] = 0
            obj.cleaned_data['comment_count'] = 0
            obj.cleaned_data['up_count'] = 0
            obj.cleaned_data['down_count'] = 0
            obj.cleaned_data['blog_id'] = blog_obj.nid
            tags = obj.cleaned_data.pop('tags')
            content = obj.cleaned_data.pop('content')
            print(obj.cleaned_data)
            res = models.Article.objects.create(**obj.cleaned_data)
            for row in tags:
                print(res.nid,row)
                models.Article2Tag.objects.create(article_id=res.nid,tag_id=row)

            models.ArticleDetail.objects.create(content=content,article_id=res.nid)


            return redirect('/manage/all.html')

        else:

            print('not ok',obj.cleaned_data)

            return render(request,'manage_add.html',{'obj':obj})



def upload_img(request):

    print(request.POST,request.FILES)
    print('zzimg')
    import os
    upload_type = request.GET.get('dir')
    file_obj = request.FILES.get('imgFile')
    file_path = os.path.join('static/img',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    # dic 规定 就是 这样写
    dic = {
        'error': 0,
        'url': '/' + file_path,
        'message': '错误了...'
    }
    print(dic)
    import json
    return HttpResponse(json.dumps(dic))







