from django.shortcuts import render, redirect, get_object_or_404
from .models import Calendar, Image, Comment, Friend, ImageComment, Notification
from accounts.models import User
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import (
    CalendarForm,
    CommentForm,
    ImageForm,
    ImageCommentForm,
)
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import JsonResponse
from datetime import datetime
import re, calendar
from .notification import comment_send_notification, imageComment_send_notification
from .templatetags.custom_tags import add_date, subtract_date, subtract_month, subtract_year

@login_required
def calendar_view(request):
    posts = Calendar.objects.all()
    calendar.setfirstweekday(6)

    year_list = [
        'first_index',
        'JANUARY',
        'FEBRUARY',
        'MARCH',
        'APRIL',
        'MAY',
        'JUNE',
        'JULY',
        'AUGUST',
        'SEPTEMBER',
        'OCTOBER',
        'NOVEMBER',
        'DECEMBER'
    ]
    today = datetime.now().date()

    year_month_str = request.GET.get('year_month', '')
    if year_month_str:
        year_month = datetime.strptime(year_month_str, "%Y-%m").date()
    else:
        year_month = datetime.today()
    year = year_month.year # example output: 2018
    month = year_month.month # example output: 10
    month_alphabet = year_list[month] # example output: October

    current_year_month = datetime.strptime((str(datetime.today().year) +"-"+ str(datetime.today().month)), "%Y-%m").date()

    month_calendar = calendar.monthcalendar(year, month)

    weeks = []
    # days = []

    for w in range(0, len(month_calendar)):
        week = month_calendar[w] # each week include its days for the given month. ex) [0, 1, 2, 3, 4, 5, 6]
        weeks.append(week)
        # for x in range(7):
        #     day = week[x]
        #     days.append(day)


    pre_month = (year_month.month - 1) % 12 or 12
    next_month = (year_month.month + 1) % 12 or 12
    next_year_month = str(year_month.year) + "-" + str(next_month)
    pre_year_month = str(year_month.year) + "-" + str(pre_month)
    if pre_month is 12:
        pre_year_month = str(year_month.year - 1) + "-" + str(pre_month)
    elif next_month is 1:
        next_year_month = str(year_month.year + 1) + "-" + str(next_month)

    pre_year_month = datetime.strptime(pre_year_month, "%Y-%m").date()
    next_year_month = datetime.strptime(next_year_month, "%Y-%m").date()


    args = {
        'year_month': year_month,
        'current_year_month': current_year_month,
        'month_alphabet': month_alphabet,
        'pre_year_month': pre_year_month,
        'next_year_month': next_year_month,
        'weeks': weeks,
        'posts': posts,
        'today': today,
    }
    return render(request, 'album/calendar_view.html', args)

class CalendarView(TemplateView):
    template_name = 'album/home.html'

    def get(self, request):

        posts = Calendar.objects.all().order_by('-date')
        thumbnail = Image.objects.all()
        form = CalendarForm(request.POST)

        # 검색 코드
        year_month =''
        year_month_str = request.GET.get('year_month', '')
        emoticon = request.GET.get('emoticon', '')
        option = request.GET.get('option', '')
        search_content = request.GET.get('search_content', '')

        if year_month_str and option == 'title':
            # date only or date and title
            year_month = datetime.strptime(year_month_str, "%Y-%m").date()
            posts = posts.filter(date__year=year_month.year, date__month=year_month.month, title__contains=search_content, emoticon__contains=emoticon)
        elif year_month_str and option == 'content':
            # date and content
            year_month = datetime.strptime(year_month_str, "%Y-%m").date()
            posts = posts.filter(date__year=year_month.year, date__month=year_month.month, description__contains=search_content, emoticon__contains=emoticon)
        elif option == 'title' and search_content:
            # title only
            posts = posts.filter(title__contains=search_content, emoticon__contains=emoticon)
        elif option == 'content' and search_content:
            # content only
            posts = posts.filter(description__contains=search_content, emoticon__contains=emoticon)
        elif emoticon:
            # emoticon only
            posts = posts.filter(emoticon__contains=emoticon)
        else:
            # Search nothing : disply posts with current year and month
            if year_month_str:
                year_month = datetime.strptime(year_month_str, "%Y-%m").date()
            else:
                year_month = datetime.strptime((str(datetime.today().year) +"-"+ str(datetime.today().month)), "%Y-%m").date()
            posts = posts.filter(date__year=year_month.year, date__month=year_month.month)

        # 이전달 / 다음달 구하기
        next_year_month = ''
        pre_year_month = ''
        if year_month:
            pre_month = (year_month.month - 1) % 12 or 12
            next_month = (year_month.month + 1) % 12 or 12
            next_year_month = str(year_month.year) + "-" + str(next_month)
            pre_year_month = str(year_month.year) + "-" + str(pre_month)
            if pre_month is 12:
                pre_year_month = str(year_month.year - 1) + "-" + str(pre_month)
            elif next_month is 1:
                next_year_month = str(year_month.year + 1) + "-" + str(next_month)


        args = {
            # 'notifications': notifications,
            'form': form,
            'year_month': year_month,
            'next_year_month': next_year_month,
            'pre_year_month': pre_year_month,
            'option': option,
            'search_content': search_content,
            'emoticon': emoticon,
            'posts': posts,
            'thumbnail': thumbnail,
        }
        return render(request, self.template_name, args)

    def post(self, request):
        return render(request, self.template_name)

@login_required
def post_new(request, date):
    if request.method == 'POST':
        form = CalendarForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # check if the post exists on selected date
            # if so, send msg to home.html
            try:
                post = get_object_or_404(Calendar, date=post.date)
                msg = 'Post on selected date already exists.'
                args = {
                    'post' : post,
                    'msg': msg,
                }

                return render(request, 'album/home.html', args)
            # if the post doesn't exist on selected date
            # create new post on that date
            except:
                post.author = request.user
                post.save()

                for img in request.FILES.getlist('image'):
                    Image.objects.create(
                        post=post,
                        image=img
                    ).save()

                return redirect('album:calendar_view')
    else:
        form = CalendarForm()

    args = {
        'form': form,
        'date': date,
        'today': datetime.now(),
    }
    return render(request, 'album/calendar_new.html', args)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Calendar, pk=pk)
    if request.user.is_superuser or request.user == post.author:
        images = Image.objects.filter(post=post)

        if request.method == "POST":
            form = CalendarForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()

                for img in request.FILES.getlist('image'):
                    Image.objects.create(
                        post=post,
                        image=img
                    ).save()

                return redirect('album:post_detail', pk=post.pk)
        else:
            form = CalendarForm(instance=post)
        args = {
            'form': form,
            'images': images,
        }
        return render(request, 'album/post_edit.html', args)
    else:
        return redirect('album:home')

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Calendar, pk=pk)
    if request.user.is_superuser or post.author == request.user:
        post.delete()
    return redirect('album:calendar_view')

class PostDetailView(TemplateView):
    template_name = 'album/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Calendar, pk=pk)
        comments = post.comments.filter(post=post, parent__isnull=True)
        form = CommentForm()
        users = User.objects.all()

        args = {
            'form': form,
            'post': post,
            'users': users,
            'comments': comments,
        }
        return render(request, self.template_name, args)

    def post(self, request, pk):
        post = get_object_or_404(Calendar, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():

            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    reply_comment = form.save(commit=False)
                    reply_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            comment_send_notification(request, post, comment, parent_id)

            form = CommentForm() # 입력후 다시 빈칸으로 만들기
            return redirect('album:post_detail', pk=post.pk)

        args =  {
            'form': form,
            'post': post,
        }
        return render(request, self.template_name, args)

class ImageDetailView(TemplateView):
    template_name = 'album/image_detail.html'

    def get(self, request, post_pk, pk):
        image = get_object_or_404(Image, pk=pk)
        comments = image.image_comments.filter(image=image, parent__isnull=True)

        try:
            previous_image = Image.objects.filter(post=image.post.pk, pk__lt=image.pk).order_by('-pk')[0]
        except:
            previous_image = Image.objects.filter(post=image.post.pk).last()
        try:
            next_image = Image.objects.filter(post=image.post.pk,pk__gt=image.pk).order_by('pk')[0]
        except:
            next_image = Image.objects.filter(post=image.post.pk).first()

        form = ImageCommentForm()
        users = User.objects.all()

        args = {
            'previous_image': previous_image,
            'next_image': next_image,
            'image': image,
            'comments': comments,
            'form': form,
            'users': users
        }
        return render(request, self.template_name, args)

    def post(self, request, post_pk, pk):
        image = get_object_or_404(Image, pk=pk)
        form = ImageCommentForm(request.POST)
        if form.is_valid():

            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = ImageComment.objects.get(id=parent_id)
                if parent_obj:
                    reply_comment = form.save(commit=False)
                    reply_comment.parent = parent_obj

            image_comment = form.save(commit=False)
            image_comment.image = image
            image_comment.author = request.user
            image_comment.save()

            imageComment_send_notification(request, image, image_comment, parent_id)

            form = ImageCommentForm() # 입력후 다시 빈칸으로 만들기
            return redirect('album:image_detail', post_pk=image.post.pk, pk=image.pk)

        args =  {'form': form, 'image': image}
        return render(request, self.template_name, args)

@login_required
def image_edit(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.user.is_superuser or request.user == image.post.author:
        if request.method == "POST":
            form = ImageForm(request.POST, instance=image)
            if form.is_valid():
                image = form.save(commit=False)
                if request.FILES:
                    image.image = request.FILES['image']
                image.save()

                return redirect('album:image_detail', post_pk=image.post.pk, pk=image.pk)
        else:
            form = ImageForm(instance=image)
        args = {
            'form': form,
        }
        return render(request, 'album/image_edit.html', args)
    else:
        return redirect('album:home')

@login_required
def image_remove(request, operation, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.user.is_superuser or image.post.author == request.user:
        image.delete()
    if operation == 'post_edit':
        return redirect('album:post_edit', pk=image.post.pk)
    elif operation == 'image_detail':
        return redirect('album:post_detail', pk=image.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_superuser or comment.author == request.user:
        comment.delete()
        Notification.objects.filter(
            post_comment=comment,
        ).delete()
    return redirect('album:post_detail', pk=comment.post.pk)

@login_required
def image_comment_remove(request, pk):
    comment = get_object_or_404(ImageComment, pk=pk)
    if request.user.is_superuser or comment.author == request.user:
        comment.delete()
        Notification.objects.filter(
            image_comment=comment,
        ).delete()
    return redirect('album:image_detail', post_pk=comment.image.post.pk, pk=comment.image.pk)

@login_required
def notification(request, operation, pk):
    if operation == 'post_comment':
        comment = get_object_or_404(Comment, pk=pk)
        notification = Notification.objects.filter(post_comment=comment).update(read=True)
        return redirect('album:post_detail', pk=comment.post.pk)
    elif operation == 'image_comment':
        image_comment = get_object_or_404(ImageComment, pk=pk)
        notification = Notification.objects.filter(image_comment=image_comment).update(read=True)
        return redirect('album:image_detail', post_pk=image_comment.image.post.pk, pk=image_comment.image.pk)
    elif operation == 'post_like':
        post = get_object_or_404(Calendar, pk=pk)
        notification = Notification.objects.filter(post=post).update(read=True)
        return redirect('album:post_detail', pk=post.pk)
    elif operation == 'image_like':
        image = get_object_or_404(Image, pk=pk)
        notification = Notification.objects.filter(image=image).update(read=True)
        return redirect('album:image_detail', post_pk=image.post.pk, pk=image.pk)

@login_required
def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)
    return redirect('accounts:view_profile_with_pk', pk=new_friend.pk)

@login_required
def like(request, operation):
    if request.method == 'POST':
        if operation == 'post':
            user = request.user # 로그인한 유저를 가져온다.
            obj_id = request.POST.get('pk', None)
            obj = Calendar.objects.get(pk = obj_id) #해당 오브젝트를 가져온다.

            if obj.likes.filter(id = user.id).exists(): #이미 해당 유저가 likes컬럼에 존재하면
                obj.likes.remove(user) #likes 컬럼에서 해당 유저를 지운다.
                message = 'You disliked this'
                if obj.author != request.user:
                    Notification.objects.filter(
                        receiver=obj.author,
                        sender=request.user,
                        post=obj,
                        like=True
                    ).delete()
            else:
                obj.likes.add(user)
                message = 'You liked this'
                if obj.author != request.user:
                    Notification.objects.create(
                        receiver=obj.author,
                        sender=request.user,
                        post=obj,
                        like=True
                    ).save()

        elif operation == 'image':
            user = request.user # 로그인한 유저를 가져온다.
            obj_id = request.POST.get('pk', None)
            obj = Image.objects.get(pk = obj_id) #해당 오브젝트를 가져온다.

            if obj.likes.filter(id = user.id).exists(): #이미 해당 유저가 likes컬럼에 존재하면
                obj.likes.remove(user) #likes 컬럼에서 해당 유저를 지운다.
                message = 'You disliked this'
                if obj.post.author != request.user:
                    Notification.objects.filter(
                        receiver=obj.post.author,
                        sender=request.user,
                        image=obj,
                        like=True
                    ).delete()
            else:
                obj.likes.add(user)
                message = 'You liked this'
                if obj.post.author != request.user:
                    Notification.objects.create(
                        receiver=obj.post.author,
                        sender=request.user,
                        image=obj,
                        like=True
                    ).save()


        likes_count = obj.likes.count()
        user_like = obj.likes.filter(id = user.id).exists()

    context = {
        'likes_count' : likes_count,
        'message' : message,
        'user_like' : user_like,
    }
    return JsonResponse(context)

@login_required
def move_post(request, date, operation):
    posts = Calendar.objects.all()

    for i in range(len(posts)):
        i += 1
        if operation == 'next':
            calculated_date = add_date(date, i)
        elif operation == 'prev':
            calculated_date = subtract_date(date, i)

        post = posts.filter(date=calculated_date)
        if post.exists():
            post = get_object_or_404(Calendar, date=calculated_date)
            return redirect('album:post_detail', pk=post.pk)
        else:
            post = get_object_or_404(Calendar, date=date)
    return redirect('album:post_detail', pk=post.pk)
