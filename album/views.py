from django.shortcuts import render, redirect, get_object_or_404
from .models import Calendar, Image, Comment, Friend, ImageComment, Notification
from accounts.models import User
from django.utils import timezone
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import (
    CalendarForm,
    CommentForm,
    ImageForm,
    ImageCommentForm,
)
from mysite.settings import TEMPLATES

class CalendarView(TemplateView):
    template_name = 'album/home.html'

    # TEMPLATES[0]['OPTIONS']['context_processors'].insert(0, "album.context_processors.notification")
    def get(self, request):

        # notifications = Notification.objects.filter(receiver=request.user).order_by('read', '-date')
        #
        # page = request.GET.get('page', 1)
        # paginator = Paginator(notifications, 5)
        # try:
        #     notifications = paginator.page(page)
        # except PageNotAnInteger:
        #     notifications = paginator.page(1)
        # except EmptyPage:
        #     notifications = paginator.page(paginator.num_pages)



        posts = Calendar.objects.all().order_by('-date')
        thumbnail = Image.objects.all()
        form = CalendarForm(request.POST)

        # 검색 코드
        title = request.GET.get('title', '')
        description = request.GET.get('description', '')
        year_month_str = request.GET.get('year_month', '')
        emoticon = request.GET.get('emoticon', '')
        if year_month_str:  # 날짜 검색했을 경우 -> year_month = 검색한 날짜
            year_month = datetime.strptime(year_month_str, "%Y-%m").date()
        else:               # 날짜 검색안했을 경우 -> year_month = 현재 날짜
            year_month = datetime.strptime((str(datetime.today().year) +"-"+ str(datetime.today().month)), "%Y-%m").date()
        posts = posts.filter(date__year=year_month.year, date__month=year_month.month, emoticon__contains=emoticon, title__contains=title, description__contains=description)

        # 이전달 / 다음달 구하기
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
            'title': title,
            'emoticon': emoticon,
            'posts': posts,
            'thumbnail': thumbnail,
        }
        return render(request, self.template_name, args)

    def post(self, request):
        return render(request, self.template_name)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = CalendarForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for img in request.FILES.getlist('image'):
                Image.objects.create(
                    post=post,
                    image=img
                ).save()

            return redirect('album:home')
    else:
        form = CalendarForm()

    args = {
        'form': form,
        'today':datetime.now(),
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
    return redirect('album:home')

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
            if post.author != request.user:
                Notification.objects.create(
                    receiver=post.author,
                    sender=request.user,
                    post_comment=comment,
                ).save()
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

            comment = form.save(commit=False)
            comment.image = image
            comment.author = request.user
            comment.save()
            if image.post.author != request.user:
                Notification.objects.create(
                    receiver=image.post.author,
                    sender=request.user,
                    image_comment=comment,
                ).save()
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
    return redirect('album:post_detail', pk=comment.post.pk)

@login_required
def image_comment_remove(request, pk):
    comment = get_object_or_404(ImageComment, pk=pk)
    if request.user.is_superuser or comment.author == request.user:
        comment.delete()
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

@login_required
def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)
    return redirect('accounts:view_profile_with_pk', pk=new_friend.pk)
