from django.shortcuts import get_object_or_404
from album.models import Calendar
from django import template
import datetime

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def add_string(a, b):
    return str(a) + str(b)

@register.filter
def combine_day(date, val):
    if val < 10:
        val = '0'+str(val)
    return str(date)+'-'+str(val)

@register.filter
def add_date(date, val):
    print('-------add_date---------')
    try:
        date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    result = date + datetime.timedelta(days=val)
    return result

@register.filter
def subtract_date(date, val):
    print('-------subtract_date---------')
    try:
        date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    result = date - datetime.timedelta(days=val)
    return result

@register.filter
def subtract_month(date, val):
    print('-------subtract_month---------')
    date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    result = date - datetime.timedelta(val*365.24/12)
    return result

@register.filter
def subtract_year(date, val):
    print('-------subtract_year---------')
    date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    result = date - datetime.timedelta(val*365.24)
    return result

@register.filter(name='zip')
def zip_lists(a, b):
    print('-------zip---------')
    return zip(a, b)

@register.filter(name='has_post')
def has_post(date_str):
    date=''
    has_post = False
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        pass
        
    posts = Calendar.objects.all()
    for post in posts:
        has_post = False
        post_date_str = str(post.date.year)+'-'+str(post.date.month)+'-'+str(post.date.day)
        post_date = datetime.datetime.strptime(post_date_str, "%Y-%m-%d").date()
        if date == post_date:
            has_post = True
            break
        else:
            has_post = False

    if has_post == True:
        return True
    else:
        return False

@register.filter(name='get_post_field')
def get_post_field(date, field):
    try:
        post = get_object_or_404(Calendar, date=date)
        post_pk = post.pk
        post_title = post.title
        image = ''
        for thumb in post.images.all():
            image = thumb.thumbnail.url
            break

        if field == 'pk':
            return post_pk
        elif field == 'title':
            return post_title
        elif field == 'image':
            return image

    except:
        post_pk = None
        return None
