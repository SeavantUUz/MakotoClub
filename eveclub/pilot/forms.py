#coding: utf-8
from django import forms
from django.forms.util import ErrorList
from pilot.models import *

class PilotErrorList(ErrorList):
    def __unicode__(self):
        return self.as_bootstrap()
    def as_bootstrap(self):
        if not self:
            return u''
        else:
            return u'<p class="alert alert-error">%s</p>' % '<br />'.join(self)

class SignupForm(forms.Form):
    error_messages = {
        'duplicate_username': u'您输入的用户名已被使用',
        'duplicate_email': u'您输入的电子邮件地址已被使用',
    }
    username = forms.RegexField(regex=r'^\S{2,}$', max_length=30, label=u'会员用户名',
                                error_messages={'required': u'请输入用户名', 'invalid': u'请输入有效的用户名'})
    email    = forms.EmailField(max_length=128, label=u'电子邮件',
                                error_messages={'required': u'请输入电子邮件地址', 'invalid': u'请输入有效的电子邮件地址'})
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Pilot.objects.get(username=username)
        except Pilot.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Pilot.objects.get(email=email)
        except Pilot.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

class UpdatePasswordForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

    error_messages = {
        'invalid_old_password': u'您输入的旧密码不正确',
        'invalid_confirm_password': u'您两次输入的新密码不一致',
    }
    old_password = forms.CharField(widget=forms.PasswordInput, label=u'旧密码',
                                   error_messages={'required': u'请输入旧的密码'})
    new_password = forms.CharField(widget=forms.PasswordInput, label=u'新密码',
                                   error_messages={'required': u'请输入新的密码'})
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=u'重复新密码',
                                       error_messages={'required': u'请再输入一次新密码'})
    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if self.request.user.check_password(old_password):
            return old_password
        raise forms.ValidationError(self.error_messages['invalid_old_password'])

    def clean_confirm_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']
        if new_password == confirm_password:
            return confirm_password
        raise forms.ValidationError(self.error_messages['invalid_confirm_password'])

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Pilot
        fields = ('gender', 'birthday', 'residence', 'yy', 'qq', 'signature')
        widgets = {'signature': forms.Textarea()}

class ForgotPasswordForm(forms.Form):
    error_messages = {
        'username_not_found': u'您输入的用户名不存在',
        'email_not_match': u'您输入的电子邮件地址和我们的记录不匹配',
    }
    username = forms.RegexField(regex=r'^\S{2,}$', max_length=30, label=u'用户名',
                                error_messages={'required': u'请输入用户名', 'invalid': u'请输入有效的用户名'})
    email    = forms.EmailField(max_length=128, label=u'电子邮件',
                                error_messages={'required': u'请输入电子邮件地址', 'invalid': u'请输入有效的电子邮件地址'})
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Pilot.objects.get(username=username)
        except Pilot.DoesNotExist:
            raise forms.ValidationError(self.error_messages['username_not_found'])
        return username

    def clean_email(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
        else:
            return ''
        email = self.cleaned_data['email']
        u = Pilot.objects.get(username=username)
        if u.email == email:
            return email
        else:
            raise forms.ValidationError(self.error_messages['email_not_match'])

class UploadGravatarForm(forms.Form):
    gravatar = forms.ImageField(label=u'上传新头像', error_messages={'required': u'请选择要上传的图片', 'invalid': u'请上传正常的图片'})
