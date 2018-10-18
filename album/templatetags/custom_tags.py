from django import template
import datetime

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def add_date(date, val):
    if val < 10:
        val = '0'+str(val)
    return str(date)+'-'+str(val)

@register.filter
def subtract_date(date, val):
    date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    result = date - datetime.timedelta(days=val)
    return result

@register.filter
def subtract_month(date, val):
    date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    result = date - datetime.timedelta(val*365.24/12)
    return result

@register.filter
def subtract_year(date, val):
    date_str = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    result = date - datetime.timedelta(val*365.24)
    return result

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

@register.filter(name='has_post')
def has_post(day_str, posts):
    day=''
    try:
        day = datetime.datetime.strptime(day_str, "%Y-%m-%d").date()
    except:
        pass

    for post in posts:
        has_post = False
        post_date_str = str(post.date.year)+'-'+str(post.date.month)+'-'+str(post.date.day)
        post_date = datetime.datetime.strptime(post_date_str, "%Y-%m-%d").date()
        if day == post_date:
            has_post = True
            break
        else:
            has_post = False

    if has_post == True:
        return True
    else:
        return False
