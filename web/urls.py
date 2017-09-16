from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$',views.index,name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/',views.signup ,name = 'signup'),
    url(r'^introduction/',views.introduction,name='introduction' ),
    url(r'^team/',views.team ,name='team'),
    url(r'^download/',views.download,name='download'),
    url(r'^user/',views.user,name='user' ),
    url(r'^contact/',views.contact,name='contact' ),
    url(r'^login/forgot/',views.forgot ),
    url(r'^personal/$', views.personal,name='personal'),
    url(r'^personal/apply/', views.apply,name='apply'),
    url(r'^personal/change/', views.change, name='change'),
    url(r'^administrator/$', views.administrator, name='administrator'),
    url(r'^personal/passwordChange/', views.password_change,name='passwordChange'),
    url(r'^personal/upload/', views.upload_file,name='upload'),
    url(r'^personal/new_apply/', views.new_apply,name='new_apply'),
    url(r'^allow_examine/', views.allow_examine,name='allow_examine'),
    url(r'^cancel_examine/', views.cancel_examine,name='cancel_examine'),
    url(r'^logout', views.logout),
]