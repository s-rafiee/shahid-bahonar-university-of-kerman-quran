from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Blogs
from django.core.paginator import Paginator
from django.db.models import Q
from activities.models import Activities, Categories


# Create your views here.


def homePage(request):
    data = dict()
    data['page'] = 'home'
    data['blogs'] = Blogs.objects.filter(status=1).order_by('id').reverse()[:4]

    data['education'] = Activities.objects.filter(
        cat_id__in=Categories.objects.filter(type=1).values_list('id', flat=True)).count()
    data['research'] = Activities.objects.filter(
        cat_id__in=Categories.objects.filter(type=2).values_list('id', flat=True)).count()
    data['ad'] = Activities.objects.filter(
        cat_id__in=Categories.objects.filter(type=3).values_list('id', flat=True)).count()

    return render(request, 'index.html', data)


def aboutus(request):
    data = dict()
    data['page'] = 'about'
    return render(request, 'aboutUs.html', data)


def contactus(request):
    data = dict()
    data['page'] = 'contact'
    return render(request, 'contactUs.html', data)


def blogs(request):
    data = dict()
    data['page'] = 'blogs'

    items = Blogs.objects.filter(status=1).order_by('id')
    paginator = Paginator(items, 10)
    this_page = request.GET.get('page', '1')
    data['blogs'] = paginator.get_page(this_page)

    return render(request, 'blogs.html', data)


def blog(request, bid):
    try:
        data = dict()
        data['blog'] = Blogs.objects.get(pk=bid)
        if data['blog'].status is 1:
            data['blogs'] = Blogs.objects.filter(~Q(id=bid))[:2]
            return render(request, 'blog.html', data)
        else:
            return render(request, '404.html')
    except Blogs.DoesNotExist:
        return render(request, '404.html')


def activists(request, type):
    data = dict()
    if type == 'education':
        items = Activities.objects.filter(cat_id__in=Categories.objects.filter(type=1).values_list('id', flat=True))
        paginator = Paginator(items, 10)
        page = request.GET.get('page')
        data['activities'] = paginator.get_page(page)
        return render(request, 'activists.html', data)
    elif type == 'research':
        items = Activities.objects.filter(cat_id__in=Categories.objects.filter(type=2).values_list('id', flat=True))
        paginator = Paginator(items, 10)
        page = request.GET.get('page')
        data['activities'] = paginator.get_page(page)
        return render(request, 'activists.html', data)
    elif type == 'ad':
        items = Activities.objects.filter(cat_id__in=Categories.objects.filter(type=3).values_list('id', flat=True))
        paginator = Paginator(items, 10)
        page = request.GET.get('page')
        data['activities'] = paginator.get_page(page)
        return render(request, 'activists.html', data)
    else:
        return render(request, '404.html')
