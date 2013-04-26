#coding: utf-8

import hashlib, os
from PIL import Image
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from eveclub.settings import MEDIA_ROOT, PROJECT_SERVER
from eveclub.lib import RequestContext
from pilot.models import *
from pilot.forms import *

def signup(request):
    if request.user.is_authenticated():
        return render_to_response('warning.html', {'message': u'您已经是EveClub的注册用户了，无需重新注册！'}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = SignupForm(request.POST, error_class=PilotErrorList)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = Pilot.objects.make_random_password()
            mail_subject = u'EveClub会员注册信息'
            mail_body = u'感谢您注册成为EveClub的会员，您的注册信息如下：\n\n用户名：%s\n密码：%s\n\n请从这里登录EveClub：http://%s/pilot/login/' % (username, password, PROJECT_SERVER)
            mail_from = u'service@eveclub.org'
            mail_to = [email,]
            user = Pilot.objects.create_user(username=username, email=email, password=password)
            user.save()
            send_mail(mail_subject, mail_body, mail_from, mail_to)
    else:
        form = SignupForm()
    return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def profile(request):
    return render_to_response('profile.html', context_instance=RequestContext(request))

@login_required
def updatepassword(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(data=request.POST, request=request, error_class=PilotErrorList)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save(update_fields=['password'])
    else:
        form = UpdatePasswordForm()
    return render_to_response('update.html', {'form': form, 'data_type': u'密码'}, context_instance=RequestContext(request))

@login_required
def updateprofile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user, error_class=PilotErrorList)
        if form.is_valid():
            form.save()
    else:
        form = UpdateProfileForm(instance=request.user)
    return render_to_response('update.html', {'form': form, 'data_type': u'个人信息'}, context_instance=RequestContext(request))

def forgot(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, error_class=PilotErrorList)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            code = Pilot.objects.make_random_password(length=16)
            expire_time = now() + timedelta(days=1)
            mail_subject = u'EveClub用户密码重置'
            mail_body = u'您好，%s！\n请使用如下链接重置您的密码：\nhttp://%s/pilot/reset/%s/' % (username, PROJECT_SERVER, code)
            mail_from = u'service@eveclub.org'
            mail_to = [email,]
            try:
                r = ResetRequest.objects.get(username=username)
                r.delete()
            except ResetRequest.DoesNotExist:
                pass
            r = ResetRequest.objects.create(username=username, code=code, expire_time=expire_time)
            send_mail(mail_subject, mail_body, mail_from, mail_to)
    else:
        form = ForgotPasswordForm()
    return render_to_response('forgot.html', {'form': form}, context_instance=RequestContext(request))

def reset(request, code):
    try:
        r = ResetRequest.objects.get(code=code)
    except ResetRequest.DoesNotExist:
        return render_to_response('warning.html', {'message': u'您不能通过这个链接重置密码！'}, context_instance=RequestContext(request))
    e = r.expire_time
    if now() > e:
        return render_to_response('warning.html', {'message': u'该重置密码链接已失效！'}, context_instance=RequestContext(request))
    u = Pilot.objects.get(username=r.username)
    password = Pilot.objects.make_random_password()
    u.set_password(password)
    u.save(update_fields=['password'])
    r.delete()
    return render_to_response('message.html', {'message_title': u'密码重置成功', 'message': u'您的新密码是：%s 请妥善保存！' % password}, context_instance=RequestContext(request))

@login_required
def updategravatar(request):
    step = request.session.get('gravatar_step', 0)
    gravatar_expire_time = request.session.get('gravatar_expire_time', now())
    m=hashlib.md5()
    m.update(request.user.username.encode('utf8'))
    filename = '%s.png' % m.hexdigest()
    filepath = '%s/%s' % ('temp', filename)
    if step == 0:
        if request.method == 'POST':
            form = UploadGravatarForm(request.POST, request.FILES, error_class=PilotErrorList)
            if form.is_valid():
                img = Image.open(request.FILES['gravatar'])
                mw = 600
                mh = 450
                if img.size[0] > mw or img.size[1] > mh:
                    #压缩图片
                    #获得原图片宽高比例
                    img_wh = float(img.size[0])/float(img.size[1])
                    #获得新的图片宽或者高
                    img_w = img.size[0]
                    img_h = img.size[1]
                    #根据新的宽或者高，计算出，新的，高或者宽
                        #初始化新的宽高参数
                    nimg_w = 0
                    nimg_h = 0
                    if img_w > mw and img_h >  mh:
                        #如果宽和高都大于规定
                        #先缩小宽
                        nimg_w = mw
                        #得到新的高
                        nimg_h = int(nimg_w / img_wh)
                        if nimg_h > mh:
                            nimg_h = mh
                            nimg_w = int(nimg_h * img_wh)
                    elif img_h > mh or img_w < mw:
                        #如果只是高大于规定
                        nimg_h = mh
                        nimg_w = int(nimg_h * img_wh)
                    elif img_w > mw or img_h < mh:
                        #如果只是宽大于规定
                        nimg_w = mw
                        nimg_h = int(nimg_w / img_wh)
                        
                    #获得新的宽和高
                    size = nimg_w ,nimg_h
                    #压缩
                    img.thumbnail(size, Image.ANTIALIAS)
                img.save(MEDIA_ROOT+filepath)
                request.session['gravatar_step'] = 1
                request.session['gravatar_expire_time'] = now()+timedelta(minutes=GRAVATAR_SESSION_MINUTES)
                return render_to_response('crop.html', {'filepath': filepath, 'extra_js': ('pilot/jquery.Jcrop.js', 'pilot/crop.js',)} , context_instance=RequestContext(request))
        else:
            if os.path.exists(MEDIA_ROOT+filepath):
                os.remove(MEDIA_ROOT+filepath)
            form = UploadGravatarForm()
            return render_to_response('update.html', {'form': form, 'data_type': u'头像'}, context_instance=RequestContext(request))
    elif step == 1:
        if request.method == "POST":
            x = int(request.POST['x'])
            y = int(request.POST['y'])
            w = int(request.POST['w'])
            h = int(request.POST['h'])
            cropbox = (x, y, x+w, y+h)
            img = Image.open(MEDIA_ROOT+filepath)
            newImg = img.crop(cropbox)
            size = GRAVATAR_SIZE, GRAVATAR_SIZE
            newImg.thumbnail(size, Image.ANTIALIAS)
            
            t = now()
            year = t.year
            path = 'gravatar/%d' % year
            if not os.path.exists(MEDIA_ROOT+path):
                os.mkdir(MEDIA_ROOT+path)
            month = t.month
            path =  '%s/%d' % (path, month)
            if not os.path.exists(MEDIA_ROOT+path):
                os.mkdir(MEDIA_ROOT+path)
            newFilename = '%s.png' % t.strftime('%d%H%M%S%f')
            newFilepath = '%s/%s' % (path, newFilename)
            newImg.save(MEDIA_ROOT+newFilepath)

            u=request.user
            oldImgPath = MEDIA_ROOT+u.gravatar.name
            if u.gravatar.name != 'gravatar/default.png' and os.path.exists(oldImgPath):
                os.remove(oldImgPath)
            u.gravatar = newFilepath
            u.save(update_fields=['gravatar'])
            del(request.session['gravatar_step'])
            del(request.session['gravatar_expire_time'])
            os.remove(MEDIA_ROOT+filepath)
            return render_to_response('crop.html', {'crop_ok': True}, context_instance=RequestContext(request))
        else:
            if now() < gravatar_expire_time and os.path.exists(MEDIA_ROOT+filepath):
                return render_to_response('crop.html', {'filepath': filepath, 'extra_js': ('pilot/jquery.Jcrop.js', 'pilot/crop.js',)} , context_instance=RequestContext(request))
            else:
                request.session['gravatar_step'] = 0
                request.session['gravatar_expire_time'] = now()
                return HttpResponseRedirect('/pilot/updategravatar/')

@login_required
def showprofile(request, uid):
    uid = int(uid)
    try:
        u = Pilot.objects.get(id=uid)
    except Pilot.DoesNotExist:
        return render_to_response('warning.html', {'message': u'您试图查看的用户不存在！'}, context_instance=RequestContext(request))
    return render_to_response('showprofile.html', {'u': u}, context_instance=RequestContext(request))
