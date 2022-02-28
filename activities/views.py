import datetime

import jdatetime
from django.shortcuts import render, reverse, redirect
from .models import Categories, Activities
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from core import helper
import jdatetime
from core.settings import STATICFILES_DIRS
from django.core.paginator import Paginator


# Create your views here.

def activities(request):
    data = dict()
    data['this_menu_tab'] = 'activities'
    if request.user.is_superuser:
        allactivities = Activities.objects.all()
        paginator = Paginator(allactivities, 10)
        page_number = request.GET.get('page', '1')
        data['activities'] = paginator.get_page(page_number)
    else:
        allactivities = Activities.objects.filter(user=request.user)
        paginator = Paginator(allactivities, 10)
        page_number = request.GET.get('page', '1')
        data['activities'] = paginator.get_page(page_number)
    return render(request, 'panel/activities.html', data)


def activities_delete(request):
    if request.method == 'POST':
        activity = Activities.objects.get(pk=request.POST.get('id'))
        if activity:
            if request.user.is_superuser or activity.user.id is request.user.id:
                activity.delete()
                return HttpResponse(1)
        return HttpResponse(0)
    return render(request, '404.html', status=404)


def get_categories(request):
    result = list()
    if request.method == 'POST':
        type = request.POST.get('type', '')
        parent = request.POST.get('parent', '')
        if helper.isInt(type):
            cats = Categories.objects.filter(parent=parent, type=type)
            for cat in cats:
                result.append({'title': cat.title, 'id': cat.id})

    return JsonResponse({'result': result})


def create_actual(request):
    data = dict()
    data['this_menu_tab'] = 'activities'
    activate = Activities()

    if request.method == "POST":
        sw = True
        old = dict()

        type = request.POST.get('type', '')
        valid_types = [1, 2, 3]
        if not helper.isInt(type) or not (int(type) in valid_types):
            sw = False
            messages.error(request, 'نوع فعالیت پژوهشی معتبر نیست.', extra_tags='danger')

        if helper.isInt(request.POST.get('group', '')):
            group = Categories.objects.filter(type=type, id=request.POST.get('group').strip()).count()
            if group is 1:
                certificate = request.POST.get('certificate', '').strip()
                if helper.isInt(certificate):
                    certifi = Categories.objects.filter(pk=request.POST.get('certificate').strip(),
                                                        parent=request.POST.get('group').strip()).count()
                    if certifi is not 1:
                        sw = False
                        messages.error(request, 'مدرک انتخابی معتبر نیست.', extra_tags='danger')
                else:
                    sw = False
                    messages.error(request, 'مدرک انتخابی معتبر نیست.', extra_tags='danger')
            else:
                sw = False
                messages.error(request, 'گروه انتخابی معتبر نیست.', extra_tags='danger')
        else:
            sw = False
            messages.error(request, 'گروه انتخابی معتبر نیست.', extra_tags='danger')

        old['exporter'] = request.POST.get('exporter', '').strip()
        if len(request.POST.get('exporter', '').strip()) is 0:
            sw = False
            messages.error(request, 'صادر کننده مدرک معتبر نیست.', extra_tags='danger')

        old['year'] = request.POST.get('year', '').strip()
        if not helper.isDate(request.POST.get('year', '').strip()):
            sw = False
            messages.error(request, 'تاریخ دریافت مدرک معتبر نیست.', extra_tags='danger')

        old['expiration'] = request.POST.get('expiration', '').strip()
        if not helper.isDate(request.POST.get('expiration', '').strip()):
            sw = False
            messages.error(request, 'تاریخ اعتبار مدرک معتبر نیست.', extra_tags='danger')
        format = ''
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
                sw = False
                messages.error(request, 'فرمت تصویر ارسالی معتبر نیست.', extra_tags='danger')
        else:
            sw = False
            messages.error(request, 'تصویری برای ارسال انتخاب نشده است.', extra_tags='danger')

        activate.user = request.user
        activate.person = 1
        activate.exporter = request.POST.get('exporter').strip()
        if sw:
            activate.image = request.FILES['image']
            activate.expiration_date = jdatetime.datetime.strptime(request.POST.get('expiration'), '%d/%m/%Y').strftime(
                '%Y-%m-%d')
            activate.start_date = jdatetime.datetime.strptime(request.POST.get('year'), '%d/%m/%Y').strftime('%Y-%m-%d')
            activate.cat = Categories.objects.get(pk=request.POST.get('certificate').strip())
            activate.save()
            messages.success(request, 'مدارک شما با موفقیت ارسال شد. منتظر تایید مدارک خود باشید.',
                             extra_tags='success')
        data['old'] = old

    return render(request, 'panel/create_actual.html', data)


def create_legal(request):
    data = dict()
    data['city'] = helper.get_City()

    data['this_menu_tab'] = 'activities'
    activate = Activities()

    if request.method == "POST":
        sw = True
        old = dict()

        type = request.POST.get('type', '')
        valid_types = [1, 2, 3]
        if not helper.isInt(type) or not (int(type) in valid_types):
            sw = False
            messages.error(request, 'نوع فعالیت پژوهشی معتبر نیست.', extra_tags='danger')

        if helper.isInt(request.POST.get('group', '')):
            group = Categories.objects.filter(type=type, id=request.POST.get('group').strip()).count()
            if group is 1:
                certificate = request.POST.get('certificate', '').strip()
                if helper.isInt(certificate):
                    certifi = Categories.objects.filter(pk=request.POST.get('certificate').strip(),
                                                        parent=request.POST.get('group').strip()).count()
                    if certifi is not 1:
                        sw = False
                        messages.error(request, 'مدرک انتخابی معتبر نیست.', extra_tags='danger')
                else:
                    sw = False
                    messages.error(request, 'مدرک انتخابی معتبر نیست.', extra_tags='danger')
            else:
                sw = False
                messages.error(request, 'گروه انتخابی معتبر نیست.', extra_tags='danger')
        else:
            sw = False
            messages.error(request, 'گروه انتخابی معتبر نیست.', extra_tags='danger')

        old['company_name'] = request.POST.get('company_name', '').strip()
        if len(request.POST.get('company_name', '').strip()) is 0:
            sw = False
            messages.error(request, 'نام موسسه معتبر نیست.', extra_tags='danger')

        old['admin_first_name'] = request.POST.get('admin_first_name', '').strip()
        if len(request.POST.get('admin_first_name', '').strip()) is 0:
            sw = False
            messages.error(request, 'نام مدیر مسئول موسسه معتبر نیست.', extra_tags='danger')

        old['admin_last_name'] = request.POST.get('admin_last_name', '').strip()
        if len(request.POST.get('admin_last_name', '').strip()) is 0:
            sw = False
            messages.error(request, 'نام خانوادگی مدیر مسئول موسسه معتبر نیست.', extra_tags='danger')

        old['admin_national_code'] = request.POST.get('admin_national_code', '').strip()
        if not helper.is_National_Code(request.POST.get('admin_national_code', '').strip()):
            sw = False
            messages.error(request, 'کد ملی مدیر مسئول موسسه معتبر نیست.', extra_tags='danger')

        old['tel'] = request.POST.get('tel', '').strip()
        if not helper.isTel(request.POST.get('tel', '').strip()):
            sw = False
            messages.error(request, 'شماره تماس موسسه معتبر نیست.', extra_tags='danger')

        old['established_year'] = request.POST.get('established_year', '').strip()
        if not helper.isDate(request.POST.get('established_year', '').strip()):
            sw = False
            messages.error(request, 'تاریخ تاسیس موسسه معتبر نیست.', extra_tags='danger')

        old['address'] = request.POST.get('address', '').strip()
        if len(request.POST.get('address', '').strip()) is 0:
            sw = False
            messages.error(request, 'آدرس موسسه معتبر نیست.', extra_tags='danger')

        old['address'] = request.POST.get('address', '').strip()
        if request.POST.get('address', '').strip() in data['city']:
            sw = False
            messages.error(request, 'شهرستان انتخاب شده معتبر نیست.', extra_tags='danger')

        old['postal_code'] = request.POST.get('postal_code', '').strip()
        if not helper.isPostalCode(request.POST.get('postal_code', '').strip()):
            sw = False
            messages.error(request, 'کد پستی موسسه معتبر نیست.', extra_tags='danger')

        format = ''
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
                sw = False
                messages.error(request, 'فرمت تصویر ارسالی معتبر نیست.', extra_tags='danger')
        else:
            sw = False
            messages.error(request, 'تصویری برای ارسال انتخاب نشده است.', extra_tags='danger')

        activate.user = request.user
        activate.person = 2
        if sw:
            activate.company_name = request.POST.get('company_name').strip()
            activate.admin_first_name = request.POST.get('admin_first_name').strip()
            activate.admin_last_name = request.POST.get('admin_last_name').strip()
            activate.admin_national_code = request.POST.get('admin_national_code').strip()
            activate.tel = request.POST.get('tel').strip()
            activate.city = request.POST.get('city').strip()
            activate.address = request.POST.get('address').strip()
            activate.postal_code = request.POST.get('postal_code').strip()
            activate.start_date = jdatetime.datetime.strptime(request.POST.get('established_year'),
                                                              '%d/%m/%Y').strftime('%Y-%m-%d')
            activate.expiration_date = jdatetime.datetime.now().strftime('%Y-%m-%d')  # is invalid data
            activate.image = request.FILES['image']
            activate.cat = Categories.objects.get(pk=request.POST.get('certificate').strip())
            activate.save()
            return redirect('dashboard_show_activitie', activate.id)
        data['old'] = old
    return render(request, 'panel/create_legal.html', data)


def activitie_change_status(request, aid):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            activity = Activities.objects.get(pk=aid)
            activity.status = request.POST.get('status')
            activity.save()
            return redirect('dashboard_show_activitie', aid)
        except Activities.DoesNotExist:
            return render(request, '404.html', status=404)
    else:
        return render(request, '404.html', status=404)


def categories(request, cid=None):
    if request.user.is_staff and request.user.is_superuser:
        data = dict()
        data['cid'] = cid
        data['this_menu_tab'] = 'categories'
        if cid:
            cat = Categories.objects.get(pk=cid)
        else:
            cat = Categories()
        if request.method == 'POST':
            sw = True
            if not len(request.POST.get('title', '').strip()):
                sw = False
                messages.error(request, 'عنوان معتبر نیست.', extra_tags='danger')
            tag = request.POST.get('tag', '').strip().replace(' ', '-').lower()
            if not len(tag):
                sw = False
                messages.error(request, 'عنوان انگلیسی معتبر نیست.', extra_tags='danger')
            oldTag = Categories.objects.filter(tag=tag)
            for old in oldTag:
                if old.id is not cid:
                    sw = False
                    messages.error(request, 'عنوان انگلیسی قبلا استفاده شده است.', extra_tags='danger')
                    break
            parent = 0
            if helper.isInt(request.POST.get('parent', '').strip()):
                p = Categories.objects.get(id=request.POST.get('parent', '').strip())
                if p:
                    parent = p.id
            type = request.POST.get('type').strip()
            valid_types = [1, 2, 3]
            if not helper.isInt(type) or not (int(type) in valid_types):
                sw = False
                messages.error(request, 'نوع گروه معتبر نیست.', extra_tags='danger')

            cat.title = request.POST.get('title').strip()
            cat.tag = tag
            cat.type = request.POST.get('type').strip()
            cat.parent = parent

            if sw:
                cat.save()
                cat = []
                if cid:
                    messages.success(request, 'تغییرات با موفقیت ذخیره شد.', extra_tags='success')
                    data['cat'] = cat
                    data['cats'] = Categories.objects.filter(parent=0)
                    data['allCats'] = Categories.objects.all()
                    return HttpResponseRedirect(reverse('dashboard_categories'))
                else:
                    messages.success(request, 'گروه جدید با موفقیت ایجاد شد.', extra_tags='success')
        data['cat'] = cat
        data['cats'] = Categories.objects.filter(parent=0)
        data['allCats'] = Categories.objects.all()
        return render(request, 'panel/categories.html', data)
    else:
        return render(request, 'errors/403.html', status=403)


def categories_delete(request):
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            id = request.POST.get('id', '')
            if helper.isInt(id):
                cat = Categories.objects.get(pk=id)
                if cat:
                    Categories.objects.filter(parent=cat.id).update(parent=0)
                    cat.delete()
                    return HttpResponse(1)
            return HttpResponse(0)
        else:
            return render(request, 'errors/404.html', status=404)
    else:
        return render(request, 'errors/403.html', status=403)


def show_activitie(request, aid):
    try:
        data = dict()
        data['activity'] = Activities.objects.get(pk=aid)
        if request.user.is_superuser:
            return render(request, 'panel/show_activitie.html', data)
        else:
            if data['activity'].user == request.user:
                return render(request, 'panel/show_activitie.html', data)
            else:
                return render(request, '404.html', status=404)
    except Activities.DoesNotExist:
        return render(request, '404.html', status=404)
