from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect,render_to_response
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.hashers import *
from django.contrib.auth.forms import PasswordChangeForm
from web.models import UserImage,History,User
from web.forms import HistoryForm
from web import forms
import os
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from license.settings import BASE_DIR
from web.forms import RegisterForm, LoginForm, UserChangeForm
from django.http import HttpResponse, HttpResponseRedirect
import json
import operator
import shutil


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', context={
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
            return render(request, 'login.html', context={
                'form': form
            })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', context={'form': RegisterForm()})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():  # RegisterForm继承了UserCreationForm， 会完成用户密码强度检查，用户是否存在的验证
            try:
                form.save(True)  # 认证通过。直接保存到数据库
                url = reverse('web:login')
                return HttpResponseRedirect(url)
            except:
                messages.error(request,'您的邮箱已注册!')
                url = reverse('web:signup')
                return HttpResponseRedirect(url)
        else:
            return render(request, 'signup.html', context={'form': form})


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

def map(request):
    return render(request, 'map.html', {})
def user(request):
    return render(request, 'user.html', {})


def forgot(request):
    return render(request, 'forgot.html', {})




@login_required
def apply(request):
    user_images = UserImage.objects.filter(user=request.user)
    if len(user_images) > 0:
        return render(request, 'apply.html', {})
    else:
        messages.error(request, '无法申请,请您上传工作证和扫描件！')
        return redirect('web:upload')


def new_apply(request):
    user_history=History.objects.filter(user=request.user,examine="未审核")
    SNnum_input=request.GET.get('SNnum')
   
    if len(user_history) == 0 :
        new_history=History()
        new_history.user=request.user
        new_history.SNnum=SNnum_input
        new_history.save()
        for_activation_history=History.objects.get(user=request.user,examine="未审核",SNnum=SNnum_input)
        a=str(for_activation_history.id)
        cur_path = os.path.abspath(os.curdir)
        path = cur_path + r'\web\static\activation\history_id_'+a
        os.mkdir(path)
    #     messages.success(request, '申请成功!')
    #     return redirect('web:apply')
    # else :
    #     messages.error(request, '您的申请正在处理,请耐心等待！')
    #     return redirect('web:apply')
    user_history2=History.objects.filter(user=request.user,SNnum=SNnum_input,examine="未审核")
    length_no_examine=len(user_history2)
    response_data = {'len':length_no_examine}  #如果申请成功就是1,申请失败则是0
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

def new_apply_delete(request):
    user_history_delete=History.objects.filter(user=request.user,examine="未审核")
    if len(user_history_delete) == 1 :
        for_activation_history=History.objects.get(user=request.user,examine="未审核")
        a=str(for_activation_history.id)
        cur_path = os.path.abspath(os.curdir)
        path = cur_path + r'\web\static\activation\history_id_'+a
        shutil.rmtree(path)
        user_history_delete.delete()
        messages.success(request, '撤销成功！')
        return redirect('web:apply')
    elif len(user_history_delete) == 0 :
        messages.error(request, '您没有可撤销的申请!')
        return redirect('web:apply')
    else :
        messages.error(request, '出现未知错误,请联系管理员')
        return redirect('web:apply')
        


def allow_examine(request):
    history_id_allow=request.GET.get('allow_history_id')
    user_history=History.objects.get(id=history_id_allow)
    user_history.examine="审核通过"
    user_history.save()
    response_data = {'examine':user_history.examine}  
    return HttpResponse(json.dumps(response_data), content_type="application/json")  
   
def cancel_examine(request):
    history_id_cancel=request.GET.get('cancel_history_id')
    user_history=History.objects.get(id=history_id_cancel)
    user_history.examine="未通过"
    user_history.save()
    response_data = {'examine':user_history.examine}
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required
def personal(request):
    admin=User.objects.get(username="admin@123.com")
    if admin==request.user:
        return redirect('web:administrator')
    else:
        history_form=forms.HistoryForm()  
        personal_historys=History.objects.filter(user = request.user)
        return render(request, "personal.html",context={"personal_historys": personal_historys})


def administrator(request):
    admin=User.objects.get(username="admin@123.com")
    if admin==request.user:
        history_form=forms.HistoryForm()   
        admin_historys=History.objects.filter(examine = "未审核")
        for history in admin_historys:
            user=history.user
            #print (user.name)
            user_images = UserImage.objects.filter(user = user)
            personal_historys=History.objects.filter(user = user,examine="审核通过"or"未通过")
            #print(personal_historys[0].user.id)
            history.user_image = user_images[0]
            history.personal_history = personal_historys
            #print(admin_historys[1].personal_history[0].user)
        return render(request, "administrator.html",context={"admin_historys": admin_historys})
    else :
        messages.error(request, '您没有进入管理员界面的权限!')
        return redirect('web:personal')

def administrator1(request):
    admin=User.objects.get(username="admin@123.com")
    if admin==request.user:
        history_form=forms.HistoryForm()   
        admin_historys=History.objects.filter(examine = "未审核")
        for history in admin_historys:
            user=history.user
            #print (user.name)
            user_images = UserImage.objects.filter(user = user)
            personal_historys=History.objects.filter(user = user,examine="审核通过"or"未通过")
            #print(personal_historys[0].user.id)
            history.user_image = user_images[0]
            history.personal_history = personal_historys
            #print(admin_historys[1].personal_history[0].user)
        return render(request, "administrator1.html",context={"admin_historys": admin_historys})
    else :
        messages.error(request, '您没有进入管理员界面的权限!')
        return redirect('web:personal')


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
            return redirect('web:change')
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
        messages.success(request, '工作证上传成功！')
        return redirect('web:upload')


def upload(request):
    return render(request, 'upload.html', {})

def user1(request):
    return render(request, 'user.1.html', {})
def statistics(request):
    return render(request, 'statistics.html', {})
def statistics1(request):
    return render(request, 'statistics1.html', {})

def edit_action(request):
    pass


def logout(request):
    auth.logout(request)
    redirect_to = '/'
    return HttpResponseRedirect(redirect_to)

def mapexam(request):
    LNUser=User.objects.filter(province="辽宁"or"辽宁省")
    LN=len(LNUser)
    HLJUser=User.objects.filter(province="黑龙江"or"黑龙江省")
    HLJ=len(HLJUser)
    JLUser=User.objects.filter(province="吉林"or"吉林省")
    JL=len(JLUser)
    JSUser=User.objects.filter(province="江苏"or"江苏省")
    JS=len(JSUser)
    SDUser=User.objects.filter(province="山东"or"山东省")
    SD=len(SDUser)
    AHUser=User.objects.filter(province="安徽"or"安徽省")
    AH=len(AHUser)
    HBUser=User.objects.filter(province="河北"or"河北省")
    HB=len(HBUser)
    HNUser=User.objects.filter(province="河南"or"河南省")
    HN=len(HNUser)
    HUBUser=User.objects.filter(province="湖北"or"湖北省")
    HUB=len(HUBUser)
    HUNUser=User.objects.filter(province="湖南"or"湖南省")
    HUN=len(HUNUser)
    JXUser=User.objects.filter(province="江西"or"江西省")
    JX=len(JXUser)
    SXUser=User.objects.filter(province="陕西"or"陕西省")
    SX=len(SXUser)
    SHXUser=User.objects.filter(province="山西"or"山西省")
    SHX=len(SHXUser)
    SCUser=User.objects.filter(province="四川"or"四川省")
    SC=len(SCUser)
    QHUser=User.objects.filter(province="青海"or"青海省")
    QH=len(QHUser)
    HAINUser=User.objects.filter(province="海南"or"海南省")
    HAIN=len(HAINUser)
    GDUser=User.objects.filter(province="广东"or"广东省")
    GD=len(GDUser)
    GZUser=User.objects.filter(province="贵州"or"贵州省")
    GZ=len(GZUser)
    ZJUser=User.objects.filter(province="浙江"or"浙江省")
    ZJ=len(ZJUser)
    FJUser=User.objects.filter(province="福建"or"福建省")
    FJ=len(FJUser)
    TWUser=User.objects.filter(province="台湾"or"台湾省")
    TW=len(TWUser)
    GSUser=User.objects.filter(province="甘肃"or"甘肃省")
    GS=len(GSUser)
    YNUser=User.objects.filter(province="云南"or"云南省")
    YN=len(YNUser)
    NMGUser=User.objects.filter(province="内蒙"or"内蒙古"or"内蒙古自治区")
    NMG=len(NMGUser)
    NXUser=User.objects.filter(province="宁夏"or"宁夏回族自治区")
    NX=len(NXUser)
    XJUser=User.objects.filter(province="新疆"or"新疆维吾尔族自治区")
    XJ=len(XJUser)
    GXUser=User.objects.filter(province="广西"or"广西壮族自治区")
    GX=len(GXUser)
    XZUser=User.objects.filter(province="西藏"or"西藏自治区")
    XZ=len(XZUser)
    BJUser=User.objects.filter(province="北京"or"北京市")
    BJ=len(BJUser)
    SHUser=User.objects.filter(province="上海"or"上海市")
    SH=len(SHUser)
    TJUser=User.objects.filter(province="天津"or"天津市")
    TJ=len(TJUser)
    CQUser=User.objects.filter(province="重庆"or"重庆市")
    CQ=len(CQUser)
    list1=[LN,HLJ,JL,JS,SD,AH,HB,HN,HUB,HUN,JX,SX,SHX,SC,QH,HAIN,GD,GZ,ZJ,FJ,TW,GS,YN,NMG,NX,XJ,XZ,GX,BJ,TJ,SH,CQ]
    list1.sort()
    list1.reverse()
    dict1={'LN':LN,'HLJ':HLJ,'JL':JL,'JS':JS,'SD':SD,'AH':AH,'HB':HB,'HN':HN,'HUB':HUB,'HUN':HUN,'JX':JX,'SX':SX,'SHX':SHX,'SC':SC,'QH':QH,'HAIN':HAIN,'GD':GD,'GZ':GZ,'ZJ':ZJ,'FJ':FJ,'TW':TW,'GS':GS,'YN':YN,'NMG':NMG,'NX':NX,'XJ':XJ,'XZ':XZ,'GX':GX,'BJ':BJ,'TJ':TJ,'SH':SH,'CQ':CQ}
    a = sorted(dict1.items(),key=lambda item:item[1],reverse = True)
    b = []
    c = []
    e = {}
    def fun1(list):
        for items in list:
            for each in items:
                if type(each) is int:
                    pass
                else:
                    c.append(each)
    fun1(a)
    for i in range(len(c)):
        if len(b) < 5 :
            b.append(250 - i*40)
        if len(b) > 4 and len(b) < 11:
            b.append(70)
        if len(b) > 10 and len(b)<13:
            b.append(40)
        if len(b) > 12:
            b.append(0)

    dict1 = dict(zip(c,b))
    response_data = {'LN':dict1['LN'],'HLJ':dict1['HLJ'],'JL':dict1['JL'],'JS':dict1['JS'],'SD':dict1['SD'],'AH':dict1['AH'],'HB':dict1['HB'],'HN':dict1['HN'],'HUB':dict1['HUB'],'HUN':dict1['HUN'],'JX':dict1['JX'],'SX':dict1['SX'],'SHX':dict1['SHX'],'SC':dict1['SC'],'QH':dict1['QH'],'HAIN':dict1['HAIN'],'GD':dict1['GD'],'GZ':dict1['GZ'],'ZJ':dict1['ZJ'],'FJ':dict1['FJ'],'TW':dict1['TW'],'GS':dict1['GS'],'YN':dict1['YN'],'NMG':dict1['NMG'],'NX':dict1['NX'],'XJ':dict1['XJ'],'XZ':dict1['XZ'],'GX':dict1['GX'],'BJ':dict1['BJ'],'TJ':dict1['TJ'],'SH':dict1['SH'],'CQ':dict1['CQ']}
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

def mapexam1(request):
    LNUser=User.objects.filter(province="辽宁"or"辽宁省")
    LN=len(LNUser)
    HLJUser=User.objects.filter(province="黑龙江"or"黑龙江省")
    HLJ=len(HLJUser)
    JLUser=User.objects.filter(province="吉林"or"吉林省")
    JL=len(JLUser)
    JSUser=User.objects.filter(province="江苏"or"江苏省")
    JS=len(JSUser)
    SDUser=User.objects.filter(province="山东"or"山东省")
    SD=len(SDUser)
    AHUser=User.objects.filter(province="安徽"or"安徽省")
    AH=len(AHUser)
    HBUser=User.objects.filter(province="河北"or"河北省")
    HB=len(HBUser)
    HNUser=User.objects.filter(province="河南"or"河南省")
    HN=len(HNUser)
    HUBUser=User.objects.filter(province="湖北"or"湖北省")
    HUB=len(HUBUser)
    HUNUser=User.objects.filter(province="湖南"or"湖南省")
    HUN=len(HUNUser)
    JXUser=User.objects.filter(province="江西"or"江西省")
    JX=len(JXUser)
    SXUser=User.objects.filter(province="陕西"or"陕西省")
    SX=len(SXUser)
    SHXUser=User.objects.filter(province="山西"or"山西省")
    SHX=len(SHXUser)
    SCUser=User.objects.filter(province="四川"or"四川省")
    SC=len(SCUser)
    QHUser=User.objects.filter(province="青海"or"青海省")
    QH=len(QHUser)
    HAINUser=User.objects.filter(province="海南"or"海南省")
    HAIN=len(HAINUser)
    GDUser=User.objects.filter(province="广东"or"广东省")
    GD=len(GDUser)
    GZUser=User.objects.filter(province="贵州"or"贵州省")
    GZ=len(GZUser)
    ZJUser=User.objects.filter(province="浙江"or"浙江省")
    ZJ=len(ZJUser)
    FJUser=User.objects.filter(province="福建"or"福建省")
    FJ=len(FJUser)
    TWUser=User.objects.filter(province="台湾"or"台湾省")
    TW=len(TWUser)
    GSUser=User.objects.filter(province="甘肃"or"甘肃省")
    GS=len(GSUser)
    YNUser=User.objects.filter(province="云南"or"云南省")
    YN=len(YNUser)
    NMGUser=User.objects.filter(province="内蒙"or"内蒙古"or"内蒙古自治区")
    NMG=len(NMGUser)
    NXUser=User.objects.filter(province="宁夏"or"宁夏回族自治区")
    NX=len(NXUser)
    XJUser=User.objects.filter(province="新疆"or"新疆维吾尔族自治区")
    XJ=len(XJUser)
    GXUser=User.objects.filter(province="广西"or"广西壮族自治区")
    GX=len(GXUser)
    XZUser=User.objects.filter(province="西藏"or"西藏自治区")
    XZ=len(XZUser)
    BJUser=User.objects.filter(province="北京"or"北京市")
    BJ=len(BJUser)
    SHUser=User.objects.filter(province="上海"or"上海市")
    SH=len(SHUser)
    TJUser=User.objects.filter(province="天津"or"天津市")
    TJ=len(TJUser)
    CQUser=User.objects.filter(province="重庆"or"重庆市")
    CQ=len(CQUser)
    list1=[LN,HLJ,JL,JS,SD,AH,HB,HN,HUB,HUN,JX,SX,SHX,SC,QH,HAIN,GD,GZ,ZJ,FJ,TW,GS,YN,NMG,NX,XJ,XZ,GX,BJ,TJ,SH,CQ]
    list1.sort()
    list1.reverse()
    dict1={'LN':LN,'HLJ':HLJ,'JL':JL,'JS':JS,'SD':SD,'AH':AH,'HB':HB,'HN':HN,'HUB':HUB,'HUN':HUN,'JX':JX,'SX':SX,'SHX':SHX,'SC':SC,'QH':QH,'HAIN':HAIN,'GD':GD,'GZ':GZ,'ZJ':ZJ,'FJ':FJ,'TW':TW,'GS':GS,'YN':YN,'NMG':NMG,'NX':NX,'XJ':XJ,'XZ':XZ,'GX':GX,'BJ':BJ,'TJ':TJ,'SH':SH,'CQ':CQ}
    a = sorted(dict1.items(),key=lambda item:item[1],reverse = True)
    b = []
    c = []
    e = {}
    def fun1(list):
        for items in list:
            for each in items:
                if type(each) is int:
                    pass
                else:
                    c.append(each)
    fun1(a)
    for i in range(len(c)):
        if len(b) < 5 :
            b.append(130 - i*15)
        if len(b) > 4 and len(b) < 11:
            b.append(70)
        if len(b) > 10 and len(b)<13:
            b.append(40)
        if len(b) > 12:
            b.append(0)

    dict1 = dict(zip(c,b))
    response_data = {'LN':dict1['LN'],'HLJ':dict1['HLJ'],'JL':dict1['JL'],'JS':dict1['JS'],'SD':dict1['SD'],'AH':dict1['AH'],'HB':dict1['HB'],'HN':dict1['HN'],'HUB':dict1['HUB'],'HUN':dict1['HUN'],'JX':dict1['JX'],'SX':dict1['SX'],'SHX':dict1['SHX'],'SC':dict1['SC'],'QH':dict1['QH'],'HAIN':dict1['HAIN'],'GD':dict1['GD'],'GZ':dict1['GZ'],'ZJ':dict1['ZJ'],'FJ':dict1['FJ'],'TW':dict1['TW'],'GS':dict1['GS'],'YN':dict1['YN'],'NMG':dict1['NMG'],'NX':dict1['NX'],'XJ':dict1['XJ'],'XZ':dict1['XZ'],'GX':dict1['GX'],'BJ':dict1['BJ'],'TJ':dict1['TJ'],'SH':dict1['SH'],'CQ':dict1['CQ']}
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

def pie(request):
    all=User.objects.all()
    list1=[]
    for i in all:
        list1.append(i.office)
    dict1={}
    for item in list1:
        dict1[item] = dict1.get(item, 0) + 1
    dict1['胸外科']=dict1['胸外科']+dict1['心胸外科']+dict1['胸心外科']+dict1['胸外']+dict1['胸科']+dict1['胸腔外科']+dict1['胸外二科']+dict1['雄心外科二病区']
    dict1.pop('心胸外科')
    dict1.pop('胸心外科')
    dict1.pop('胸外')
    dict1.pop('胸科')
    dict1.pop('胸腔外科')
    dict1.pop('胸外二科')
    dict1.pop('雄心外科二病区')
    dict1.pop('')
    a = sorted(dict1.items(),key=lambda item:item[1],reverse = True)
    b = []
    c = []
    e = {}
    def fun1(list):
        for items in list:
            for each in items:
                if type(each) is int:
                    b.append(each)
                else:
                    c.append(each)
    fun1(a)
    dict_top6_name={}
    dict_top6_vue={}
    dict_top6_name['name1']=c[0]
    dict_top6_name['name2']=c[1]
    dict_top6_name['name3']=c[2]
    dict_top6_name['name4']=c[3]
    dict_top6_name['name5']=c[4]
    dict_top6_name['name6']=c[5]
    dict_top6_vue['vue1']=b[0]
    dict_top6_vue['vue2']=b[1]
    dict_top6_vue['vue3']=b[2]
    dict_top6_vue['vue4']=b[3]
    dict_top6_vue['vue5']=b[4]
    dict_top6_vue['vue6']=b[5]

    name_vue=dict(dict_top6_name, **dict_top6_vue)
    return HttpResponse(json.dumps(name_vue), content_type="application/json")


def pie2(request):
    all=User.objects.all()
    list2=[]
    for i in all:
        list2.append(i.post)
    dict2={}
    for item in list2:
        dict2[item] = dict2.get(item, 0) + 1
    dict2.pop('')
    dict2.pop('无')
    dict2['主任']=dict2['主任']+dict2['科主任']
    dict2.pop('科主任')
    a = sorted(dict2.items(),key=lambda item:item[1],reverse = True)
    b = []
    c = []
    e = {}
    def fun1(list):
        for items in list:
            for each in items:
                if type(each) is int:
                    b.append(each)
                else:
                    c.append(each)
    fun1(a)
    dict_top6_name={}
    dict_top6_vue={}
    dict_top6_name['name1']=c[0]
    dict_top6_name['name2']=c[1]
    dict_top6_name['name3']=c[2]
    dict_top6_name['name4']=c[3]
    dict_top6_name['name5']=c[4]
    dict_top6_name['name6']=c[5]
    dict_top6_vue['vue1']=b[0]
    dict_top6_vue['vue2']=b[1]
    dict_top6_vue['vue3']=b[2]
    dict_top6_vue['vue4']=b[3]
    dict_top6_vue['vue5']=b[4]
    dict_top6_vue['vue6']=b[5]

    name_vue=dict(dict_top6_name, **dict_top6_vue)
    return HttpResponse(json.dumps(name_vue), content_type="application/json")

def pie3(request):
    all=User.objects.all()
    list3=[]
    for i in all:
        list3.append(i.professional)
    dict3={}
    for item in list3:
        dict3[item] = dict3.get(item, 0) + 1
    dict3.pop('')
    a = sorted(dict3.items(),key=lambda item:item[1],reverse = True)
    b = []
    c = []
    e = {}
    def fun1(list):
        for items in list:
            for each in items:
                if type(each) is int:
                    b.append(each)
                else:
                    c.append(each)
    fun1(a)
    dict_top6_name={}
    dict_top6_vue={}
    dict_top6_name['name1']=c[0]
    dict_top6_name['name2']=c[1]
    dict_top6_name['name3']=c[2]
    dict_top6_name['name4']=c[3]
    dict_top6_name['name5']=c[4]
    dict_top6_name['name6']=c[5]
    dict_top6_vue['vue1']=b[0]
    dict_top6_vue['vue2']=b[1]
    dict_top6_vue['vue3']=b[2]
    dict_top6_vue['vue4']=b[3]
    dict_top6_vue['vue5']=b[4]
    dict_top6_vue['vue6']=b[5]
    name_vue=dict(dict_top6_name, **dict_top6_vue)
    return HttpResponse(json.dumps(name_vue), content_type="application/json")

