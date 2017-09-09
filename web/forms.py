from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import widgets

from web.models import User


class LoginForm(AuthenticationForm):
    def __str__(self):
        return self.cleaned_data['username']

    def __init__(self, *args, **kwargs):
        """

        :rtype: object
        """
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label='邮箱/手机号码',
                                                  widget=widgets.TextInput(attrs={
                                                      'placeholder':'邮箱/手机号码',
                                                      'autofocus':True
                                                  }))
        self.fields['password'] = forms.CharField(label='密码',
                                                  widget=widgets.PasswordInput(attrs={
                                                      'placeholder':'密码',
                                                  }))


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['username'] = forms.CharField(label="邮箱/手机号码：",
                                                  widget=widgets.TextInput(
                                                      attrs={'placeholder': "邮箱/手机号码","required":True}))
        self.fields['password1'] =forms.CharField(label="密码：",
                                                  widget=widgets.PasswordInput(
                                                      attrs={'placeholder': "密码","required":True}))
        self.fields['password2'] = forms.CharField(label="确认密码：",
                                                  widget=widgets.PasswordInput(
                                                      attrs={'placeholder': "确认密码","required":True}))
        self.fields['name'] = forms.CharField(label="真实姓名：",
                                                  widget=widgets.TextInput(
                                                      attrs={'placeholder': "真实姓名","required":True}))
        self.fields['unit'] = forms.CharField(label="单位：",
                                                  widget=widgets.TextInput(
                                                      attrs={'placeholder': "单位","required":True}))
        self.fields['office'] = forms.CharField(label="科室：",
                                                  widget=widgets.TextInput(
                                                      attrs={'placeholder': "科室","required":True}))
        self.fields['post'] = forms.CharField(label="职务：",
                                                  widget=widgets.TextInput(
                                                      attrs={'placeholder': "职务","required":True}))
        self.fields['professional'] = forms.CharField(label="职称：",
                                                  widget=widgets.TextInput(
                                                      attrs={'placeholder': "职称","required":True}))
        self.fields['number'] = forms.CharField(label="工号：",
                                                  widget=widgets.TextInput(
                                                      attrs={'placeholder': "工号","required":True}))



    class Meta:
        model = get_user_model()
        fields = ("name",)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.name = self.cleaned_data["name"]
        user.username = self.cleaned_data["username"]
        # user.phone = self.cleaned_data["phone"]
        user.unit = self.cleaned_data["unit"]
        user.office = self.cleaned_data["office"]
        user.post = self.cleaned_data["post"]
        user.professional = self.cleaned_data["professional"]
        user.number = self.cleaned_data["number"]
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name','unit', 'office', 'post', 'professional', 'number')


class ChangePasswordForm(forms.Form):
    oldPassword = forms.CharField()
    newPassword = forms.CharField()
    newpassword1 = forms.CharField()