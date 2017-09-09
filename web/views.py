from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.hashers import *
from django.contrib.auth.forms import PasswordChangeForm
from  web.models import UserImage
import os

from license.settings import BASE_DIR
from web.forms import RegisterForm, LoginForm, UserChangeForm
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
            form.save(True)  # 认证通过。直接保存到数据库
            url = reverse('web:login')
            return HttpResponseRedirect(url)
        else:
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


@login_required
def personal(request):
    return render(request, 'personal.html', {})


def apply(request):
    return render(request, 'apply.html', {})


@login_required
@transaction.atomic
def change(request):
    if request.method == 'GET':
        return render(request, 'change.html', context={'form': UserChangeForm(instance=request.user)})
    else:
        user_form = UserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, '修改成功！')
            return redirect('web:personal')
        else:
            messages.error(request, '修改失败，请完善所有信息！')
            return redirect('web:change')


@login_required
def password_change(request):
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
        return render(request, 'passwordChange.html', context={'form': form})
    else:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save(commit=True)
            update_session_auth_hash(request, user)
            messages.success(request, '密码修改成功！')
            return redirect('web:personal')

        else:
            messages.error(request, '密码修改失败！')
            return redirect('web:passwordChange')


@login_required
def upload_file(request):
    def file_save(file, username, path):
        upload_filename = file.name
        upload_file_type = upload_filename.split('.')[-1]
        save_image_name = username + '.' + upload_file_type
        upload_file_path = os.path.join(BASE_DIR, 'web', 'static', 'images', path, save_image_name)
        with open(upload_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return "images/{}/".format(path) + save_image_name

    def handle_uploaded_file(file_photo, file_scanning_copy, username, user):
        user_image = UserImage.objects.filter(user=user)
        static_image_path = file_save(file_photo, username, 'photo')
        static_scanning_copy_path = file_save(file_scanning_copy, username, 'scanning_copy')
        if len(user_image) == 1:
            user_image[0].user_image_path = static_image_path
            user_image[0].user_scanning_copy_path = static_scanning_copy_path
            user_image[0].save()
        else:
            user_image = UserImage(user=user, user_image_path=static_image_path,
                                   user_scanning_copy_path=static_scanning_copy_path)
            user_image.save()

    if request.method == 'GET':
        return render(request, 'upload.html', context={})
    else:
        print('ok1')
        handle_uploaded_file(request.FILES['scanning_copy_file'],request.FILES['photo_file'], request.user.username, request.user)
        messages.success(request, '个人照片上传成功！')
        return redirect('web:personal')


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
