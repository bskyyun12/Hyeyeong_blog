from album.models import Notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from django.utils import timezone

# inflect package: Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words. -> pip install inflect
# but i just need basic plural
def pluralize(num, word):
    if num > 1:
        return str(num)+' '+word+'s'
    else:
        return str(num)+' '+word

def notification(request):
    notifications =[]
    notification_lists = []
    unread_count = ''
    if request.user.is_authenticated:

        notifications = Notification.objects.filter(receiver=request.user).order_by('read', '-date')
        page = request.GET.get('page', 1)
        paginator = Paginator(notifications, 5)
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)

        date_notify = []
        minutes = 60
        hours = 60 * minutes
        days = 24 * hours
        weeks = 7 * days
        diff = timedelta(days=6)
        date_format = "%m/%d/%Y"
        today = timezone.now()

        for notify in notifications:
            sent_date = notify.date
            diff = today - sent_date

            weeks_past = int(diff.total_seconds() / weeks)
            days_past = int(diff.total_seconds() / days)
            hours_past = int(diff.total_seconds() / hours)
            minutes_past = int(diff.total_seconds() / minutes)
            seconds_past = int(diff.total_seconds())

            if weeks_past > 0:
                date_notify.append(pluralize(weeks_past, 'week')+' ago')
            elif days_past > 0:
                date_notify.append(pluralize(days_past, 'day')+' ago')
            elif hours_past > 0:
                date_notify.append(pluralize(hours_past, 'hour')+' ago')
            elif minutes_past > 0:
                date_notify.append(pluralize(minutes_past, 'minute')+' ago')
            else:
                if seconds_past < 30:
                    date_notify.append('Just now')
                else:
                    date_notify.append(pluralize(seconds_past, 'second')+' ago')

        notification_lists = zip(notifications, date_notify)

        unread_count = Notification.objects.filter(read=False).count()

    return {
        'notifications': notifications,
        'notification_lists': notification_lists,
        'unread_count': unread_count,
    }
