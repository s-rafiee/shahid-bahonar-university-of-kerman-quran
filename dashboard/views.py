import re
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from customLogin.models import MyUser
from django.urls import reverse
from core import helper
import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from activities.models import Activities
from django.conf import settings
import jdatetime
from django.db.models import Q
from blog.models import Blogs

# Create your views here.
def login_page(request):
    data = dict()
    request.session['user_mobile'] = None
    if request.method == 'POST':
        if 'mobile' in request.POST:
            mobile = request.POST.get('mobile')
            if not helper.isPhone(mobile):
                messages.error(request, 'شماره تلفن معتبر نیست. (فرمت صحیح: 09000000000)', extra_tags='danger')
                return redirect(reverse('login_page'))
            try:
                user = MyUser.objects.get(mobile=mobile)
                # Send OPT
                def_time = datetime.datetime.now() - user.otp_create_time
                if def_time.seconds > 180:
                    otp = helper.get_random_otp()
                    helper.send_otp(mobile, otp)
                    # Save OPT
                    user.otp = otp
                    user.otp_create_time = datetime.datetime.now()
                    user.save()
                # Redirect to Verify Page
                request.session['user_mobile'] = user.mobile
                return redirect(reverse('mobile_verify'))
            except MyUser.DoesNotExist:
                mobile = request.POST.get('mobile')
                user = MyUser()
                user.mobile = mobile
                # Send OPT
                otp = helper.get_random_otp()
                helper.send_otp(mobile, otp)
                # Save OPT
                user.otp = otp
                user.is_active = False
                user.save()
                # Redirect to Verify Page
                request.session['user_mobile'] = user.mobile
                return redirect(reverse('mobile_verify'))
    return render(request, 'panel/login.html')


def mobile_verify(request):
    data = dict()
    mobile = request.session.get('user_mobile', None)
    data['mobile'] = mobile
    if mobile is None:
        return redirect(reverse('login_page'))
    if request.method == 'POST':
        code = request.POST.get('opt', '')
        if helper.isInt(code) and 1000 <= int(code) <= 9999:
            try:
                user = MyUser.objects.get(mobile=mobile)
                now = datetime.datetime.now()
                otp_time = user.otp_create_time
                def_time = now - otp_time
                if def_time.seconds < 180:
                    if user.otp != int(code):
                        messages.error(request, "کد یکبار مصرف معتبر نیست.", extra_tags='danger')
                        return redirect(reverse('mobile_verify'))
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('dashboard'))
                else:  # otp time out
                    messages.error(request, "زمان استفاده از کد یکبار مصرف گذشته، درخواست کد جدید بدهید.",
                                   extra_tags='danger')
                    return redirect(reverse('mobile_verify'))
            except MyUser.DoesNotExist:
                return redirect(reverse('login_page'))
        else:
            messages.error(request, "کد یکبار مصرف معتبر نیست.", extra_tags='danger')
            return redirect(reverse('mobile_verify'))
    else:
        return render(request, 'panel/verify.html', data)


def change_verify_code(request):
    mobile = request.session.get('user_mobile', None)
    try:
        user = MyUser.objects.get(mobile=mobile)
        # Send OPT
        def_time = datetime.datetime.now() - user.otp_create_time
        if def_time.seconds > 180:
            otp = helper.get_random_otp()
            helper.send_otp(mobile, otp)
            # Save OPT
            user.otp = otp
            user.otp_create_time = datetime.datetime.now()
            user.save()
            messages.success(request, 'کد جدید به شماره ' + mobile + ' ارسال شد.', extra_tags='success')
            return redirect(reverse('mobile_verify'))
        else:
            messages.error(request, 'به تازگی کد یکبار مصرف برای شما ارسال شده است.', extra_tags='warning')
            return redirect(reverse('mobile_verify'))
    except:
        messages.error(request, 'شماره موبایل معتبر نست.', extra_tags='warning')
        return redirect(reverse('mobile_verify'))


def dashboard(request):
    data = dict()
    data['this_menu_tab'] = 'dashboard'
    if request.user.is_superuser:
        data['users'] = MyUser.objects.count()
        data['blogs'] = Blogs.objects.count()
        data['actual'] = Activities.objects.filter(person=1).count()
        data['legal'] = Activities.objects.filter(person=2).count()
    else:
        data['all'] = Activities.objects.count()
        data['reject'] = Activities.objects.filter(status=1).count()
        data['accept'] = Activities.objects.filter(status=2).count()
        data['no_process'] = Activities.objects.filter(status=0).count()
    return render(request, 'panel/dashboard.html', data)


def users(request):
    if request.user.is_superuser:
        data = dict()
        data['this_menu_tab'] = 'users'
        items = MyUser.objects.all()
        paginator = Paginator(items, 10)
        this_page = request.GET.get('page', 1)
        data['users'] = paginator.get_page(this_page)
        return render(request, 'panel/users.html', data)
    else:
        return render(request, '404.html')


def users_delete(request):
    if request.method == 'POST' and request.user.is_superuser:
        user = MyUser.objects.get(pk=request.POST.get('id', ''))
        if request.user.id is not request.POST.get('id', '') and user:
            activities = Activities.objects.filter(user=user)
            for activity in activities:
                os.remove(os.path.join(settings.MEDIA_ROOT, activity.image))

            # user.image.delete()
            return HttpResponse(1)
        return HttpResponse(0)
    else:
        return render(request, '404.html')


def profile(request, uid=0):
    data = dict()
    data['this_menu_tab'] = 'profile'
    data['user'] = request.user
    if data['user'].completed == True:
        data['user'].birthday = jdatetime.datetime.strptime(helper.toJalali(data['user'].birthday),
                                                            '%Y/%m/%d %H:%M:%S').strftime('%d/%m/%Y')
    data['city'] = helper.get_City()
    if request.method == 'POST':
        user = MyUser.objects.get(id=data['user'].id)
        sw = True
        data['user'].first_name = request.POST.get('name', '')
        if len(request.POST.get('name', '').strip()):
            user.first_name = request.POST.get('name', '').strip()
        else:
            sw = False
            messages.error(request, 'نام معتبر نیست', extra_tags='danger')

        data['user'].last_name = request.POST.get('last_name', '')
        if len(request.POST.get('last_name', '').strip()):
            user.last_name = request.POST.get('last_name', '').strip()
        else:
            sw = False
            messages.error(request, 'نام خانوادگی معتبر نیست', extra_tags='danger')
        if not request.user.completed or request.user.is_superuser:
            data['user'].national_code = request.POST.get('national_code', '')
            if helper.is_National_Code(request.POST.get('national_code', '').strip()):
                if MyUser.objects.filter(
                        national_code=request.POST.get('national_code') and ~Q(id=request.user.id)).count() == 0:
                    user.national_code = request.POST.get('national_code', '').strip()
                else:
                    sw = False
                    messages.error(request, 'این کد ملی قبلا با شماره دیگری ثبت شده است.', extra_tags='danger')
            else:
                sw = False
                messages.error(request, 'کد ملی معتبر نیست', extra_tags='danger')

        if request.POST.get('gender', '') in ['man', 'female']:
            if request.POST.get('gender') == 'man':
                user.gender = True
                data['user'].gender = True
            else:
                user.gender = False
                data['user'].gender = False
        else:
            sw = False
            messages.error(request, 'جنسیت معتبر نیست', extra_tags='danger')

        data['user'].father = request.POST.get('father', '')
        if len(request.POST.get('father', '').strip()):
            user.father = request.POST.get('father').strip()
        else:
            sw = False
            messages.error(request, 'نام پدر معتبر نیست', extra_tags='danger')

        data['user'].birthday = request.POST.get('birthday', '').strip()
        if helper.isDate(request.POST.get('birthday', '').strip()):
            user.birthday = request.POST.get('birthday', '').strip()
        else:
            sw = False
            messages.error(request, 'تاریخ تولد معتبر نیست.', extra_tags='danger')

        data['user'].city = request.POST.get('city', '').strip()
        if request.POST.get('city', '').strip() in data['city']:
            user.city = request.POST.get('city', '').strip()
        else:
            sw = False
            messages.error(request, 'شهر محل سکونت معتبر نیست.', extra_tags='danger')

        data['user'].address = request.POST.get('address', '')
        if len(request.POST.get('address', '').strip()):
            user.address = request.POST.get('address', '').strip()
        else:
            sw = False
            messages.error(request, 'آدرس معتبر نیست', extra_tags='danger')

        data['user'].postal_code = request.POST.get('postal_code', '').strip()
        if helper.isPostalCode(request.POST.get('postal_code', '').strip()):
            user.postal_code = request.POST.get('postal_code', '').strip()
        else:
            sw = False
            messages.error(request, 'کد پستی معتبر نیست.', extra_tags='danger')

        data['user'].email = request.POST.get('mail', '').strip()
        if helper.isMail(request.POST.get('mail', '').strip()):
            user.email = request.POST.get('mail', '').strip()
        else:
            sw = False
            messages.error(request, 'ایمیل معتبر نیست.', extra_tags='danger')

        data['user'].tel = request.POST.get('tel', '').strip()
        if helper.isTel(request.POST.get('tel', '').strip()):
            user.tel = request.POST.get('tel', '').strip()
        else:
            sw = False
            messages.error(request, 'شماره ثابت معتبر نیست.', extra_tags='danger')

        if 'image' in request.FILES:
            image = request.FILES['image'].name

            valid_format = ['png', 'jpg', 'jpeg']
            format = image.split('.')[-1]
            if format in valid_format:
                if not (3000 < int(request.FILES['image'].size / 1000)) and not (
                        int(request.FILES['image'].size / 1000) > 1):
                    sw = False
                    messages.error(request, 'حجم تصویر باید کمتر از 3 مگابایت باشد.', extra_tags='danger')
                else:
                    user.image = request.FILES['image']
            else:
                sw = False
                messages.error(request, 'فرمت تصویر ارسالی معتبر نیست.', extra_tags='danger')
        else:
            if not request.user.completed or not request.user.is_superuser:
                sw = False
                messages.error(request, 'تصویری برای ارسال انتخاب نشده است.', extra_tags='danger')

        if sw:
            user.completed = True
            user.birthday = jdatetime.datetime.strptime(request.POST.get('birthday'),
                                                        '%d/%m/%Y').togregorian().strftime('%Y-%m-%d')
            user.save()
            messages.success(request, 'اطلاعات حساب شما بروز رسانی شد.', extra_tags='success')
            return render(request, 'panel/profile.html', data)
        else:
            # messages.success(request, 'اطلاعات حساب شما بروز رسانی شد.', extra_tags='success')
            return render(request, 'panel/profile.html', data)
    else:
        return render(request, 'panel/profile.html', data)
