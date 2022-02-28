from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from blog.models import Blogs
from django.core.paginator import Paginator


# Create your views here.
def blogs(request):
    if request.user.is_superuser:
        data = dict()
        data['this_menu_tab'] = 'blogs'
        items = Blogs.objects.all()
        paginator = Paginator(items, 10)
        this_page = request.GET.get('page', '1')
        data['blogs'] = paginator.get_page(this_page)
        return render(request, 'panel/blogs.html', data)
    else:
        return render(request, '404.html', status=404)


def create_blog(request, bid=0):
    if request.user.is_superuser:
        data = dict()
        data['this_menu_tab'] = 'blogs'
        sw = True
        data['id'] = bid
        if bid:
            blog = Blogs.objects.get(pk=bid)
        else:
            blog = Blogs()
        data['blog'] = blog
        if request.method == 'POST':
            blog.title = request.POST.get('title', '').strip()
            if len(request.POST.get('title', '').strip()) == 0:
                sw = False
                messages.error(request, 'عنوان نوشته نمی تواند خالی باشد', extra_tags='danger')
            elif len(request.POST.get('title', '').strip()) > 60:
                sw = False
                messages.error(request, 'عنوان نوشته نمی تواند بیشتر از 60 کاراکتر باشد.', extra_tags='danger')

            blog.description = request.POST.get('description', '').strip()
            if len(request.POST.get('description', '').strip()) == 0:
                sw = False
                messages.error(request, 'خلاصه نوشته نمی تواند خالی باشد', extra_tags='danger')
            elif len(request.POST.get('description', '').strip()) > 256:
                sw = False
                messages.error(request, 'خلاصه نوشته نمی تواند بیشتر از 256 کاراکتر باشد.', extra_tags='danger')

            blog.body = request.POST.get('body', '')

            if 'image' in request.FILES:
                image = request.FILES['image'].name

                valid_format = ['png', 'jpg', 'jpeg', 'gif']
                format = image.split('.')[-1]
                if format in valid_format:
                    if not (4000 < int(request.FILES['image'].size)):
                        sw = False
                        messages.error(request, 'حجم تصویر باید کمتر از 4 مگابایت باشد.', extra_tags='danger')
                    else:
                        blog.image = request.FILES['image']
                else:
                    sw = False
                    messages.error(request, 'فرمت تصویر شاخص معتبر نیست.', extra_tags='danger')
            elif bid == 0:
                sw = False
                messages.error(request, 'تصویری شاخص انتخاب نشده است.', extra_tags='danger')
            if sw:
                blog.save()
                messages.error(request, 'با موفقیت ذخیره شد', extra_tags='success')
                data['blog'] = []
        return render(request, 'panel/create_blog.html', data)

    else:
        return render(request, '404.html', status=404)


def delete_blogs(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            blog = Blogs.objects.get(pk=request.POST.get('id', '0'))
            blog.delete()
            return HttpResponse(1)
        else:
            return HttpResponse(0, status=404)
    else:
        return render(request, '404.html', status=404)


def change_status_blogs(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            blog = Blogs.objects.get(pk=request.POST.get('id', '0'))
            if blog:
                if blog.status is 0:
                    blog.status = 1
                else:
                    blog.status = 0
                blog.save()
                return HttpResponse(blog.status)
            else:
                return HttpResponse(0, status=404)
        else:
            return HttpResponse(0, status=404)
    else:
        return render(request, '404.html', status=404)
