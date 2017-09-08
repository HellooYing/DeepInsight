from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth, messages

from web.forms import RegisterForm, LoginForm, UserChangeForm
from web.models import User
from . import templates
from django.http import HttpResponse, HttpResponseRedirect


def login(request):
    if request.method == 'GET':
        return render(request, 'login1.html', context={
            'form': LoginForm(),
        })
    else:
        form = LoginForm(data=request.POST, request=request)  # 需要传的参数是data+request， 只传data是不够的!
        if form.is_valid():  # LoginForm继承了AuthenticationForm, 会自动完成认证
            auth.login(request, form.get_user())
            # 将用户登陆
            redirect_to = request.GET.get(key='next', default=reverse('web:personal'))  # 重定向到要访问的地址，没有的话重定向到首页
            return HttpResponseRedirect(redirect_to)
        else:  # 认证失败
            return render(request, 'login1.html', context={
                'form': form
            })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup1.html', context={'form': RegisterForm()})
    else:
        print(request.POST.get('username'))
        form = RegisterForm(request.POST)
        if form.is_valid():  # RegisterForm继承了UserCreationForm， 会完成用户密码强度检查，用户是否存在的验证
            print('ok')
            form.save(True)  # 认证通过。直接保存到数据库
            url = reverse('web:login')
            return HttpResponseRedirect(url)
        else:
            print(form.fields.get('username'))
            print(form.fields.get('unit'))
            print(form.fields.get('phone'))
            print(form.fields.get('office'))
            print(form.fields.get('professional'))
            print(form.fields.get('post'))
            return render(request, 'signup1.html', context={'form': form})


def index(request):
    # return HttpResponseRedirect('')
    return render(request, 'index.html', {})


def introduction(request):
    return render(request, 'introduction.html', {})


def team(request):
    return render(request, 'team.html', {})


def download(request):
    return render(request, 'download.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def user(request):
    return render(request, 'user.html', {})


def forgot(request):
    return render(request, 'forgot.html', {})


def personal(request):
    return render(request, 'personal.html', {})


def apply(request):
    return render(request, 'apply.html', {})


@login_required
@transaction.atomic
def change(request):
    if request.method == 'GET':
        print('ok')
        return render(request, 'change.html', context={'form':UserChangeForm(instance=request.user)})
    else:
        user_form = UserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, '修改成功！')
            return redirect('web:personal')
        else:
            messages.error(request, '修改失败，请完善所有信息！')
            return redirect('web:change')


def mima(request):
    return render(request, 'mima.html', {})


def upload(request):
    return render(request, 'upload.html', {})


def administrator(request):
    return render(request, 'administrator.html', {})


def edit_action(request):
    pass


def logout(request):
    auth.logout(request)
    redirect_to = '/'
    return HttpResponseRedirect(redirect_to)
