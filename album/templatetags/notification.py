from album.models import Notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django import template

register = template.Library()

@register.inclusion_tag('album/home.html')
def notification():
    print(111111111111111111111111111111111111111)
    notifications = Notification.objects.all()

    # notifications = Notification.objects.filter(receiver=request.user).order_by('read', '-date')

    # page = request.GET.get('page', 1)
    # paginator = Paginator(notifications, 5)
    # try:
    #     notifications = paginator.page(page)
    # except PageNotAnInteger:
    #     notifications = paginator.page(1)
    # except EmptyPage:
    #     notifications = paginator.page(paginator.num_pages)

    print(111111111111111111)

    return {
        'notifications': notifications,
    }
