from django.shortcuts import render,redirect,HttpResponse
from app02 import models
# Create your views here.

def test(request):
    # objs = [
    #     models.User(username='张明',password='ab123456',email='123@qq.com'),
    #     models.User(username='小刘',password='ab123456',email='123@qq.com'),
    #     models.User(username='小夏',password='ab123456',email='123@qq.com'),
    #     models.User(username='刘明',password='ab123456',email='123@qq.com'),
    #     models.User(username='张高',password='ab123456',email='123@qq.com'),
    # ]
    # models.User.objects.bulk_create(objs,5)


    role_list = models.User2Role.objects.filter(user__username='张高').values_list('role_id')
    print(role_list)





    # permission_list = models.Permission2Action2Role.objects.filter(role__users__user_id=5).values("action__caption",
    #                                                                                    "permission__caption")
    # permission_list = models.Permission2Action2Role.objects.filter(role__users__user__username='张高').values("action__caption",
    #                                                                                    "permission__caption")
    permission_list = models.Permission2Action2Role.objects.filter(role__users__user__username='张高').values("action__caption","permission__caption")
    print(permission_list)







    return HttpResponse('test ok')