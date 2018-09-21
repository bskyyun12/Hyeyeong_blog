from django.shortcuts import render, redirect, get_object_or_404
from .models import Calendar, Comment, Friend
from accounts.models import User
from django.utils import timezone
from datetime import datetime
from django.views.generic import TemplateView
from .filters import CalendarFilter
from django.contrib.auth.decorators import login_required
from .forms import (
    CalendarForm,
    CommentForm
)

class CalendarView(TemplateView):
    template_name = 'album/home.html'

    def get(self, request):
        current_year = datetime.today().year
        current_month = datetime.today().month
        posts = Calendar.objects.all().order_by('-date')
        # posts = Calendar.objects.filter(date__year=current_year, date__month=current_month).order_by('date')

        title = request.GET.get('title', '')
        year_month_str = request.GET.get('year_month', '')



        if title and year_month_str or year_month_str:
            year_month = datetime.strptime(year_month_str, "%Y-%m").date()
            posts = posts.filter(date__year=year_month.year, date__month=year_month.month)
        elif title:
            year_month = datetime.strptime((str(current_year) +"-"+ str(current_month)), "%Y-%m").date()
            posts = posts.filter(title=title)
        # elif year_month_str:
        #     year_month = datetime.strptime(year_month_str, "%Y-%m").date()
        #     posts = posts.filter(date__year=year_month.year, date__month=year_month.month)

        else:
            year_month = datetime.strptime((str(current_year) +"-"+ str(current_month)), "%Y-%m").date()
            posts = posts.filter(date__year=year_month.year, date__month=year_month.month)
            next_year_month = datetime.strptime((str(current_year) +"-"+ str(current_month)), "%Y-%m").date().month + 1
            pre_year_month = datetime.strptime((str(current_year) +"-"+ str(current_month)), "%Y-%m").date().month - 1

        pre_year = ''
        next_year = ''
        if year_month.month == 1:
            pre_year = year_month.year - 1
            pre_month = year_month.month + 11
            next_year = year_month.year
            next_month = year_month.month + 1
        elif year_month.month == 12:
            pre_year = year_month.year
            pre_month = year_month.month - 1
            next_year = year_month.year + 1
            next_month = year_month.month - 11
        else:
            next_year = year_month.year
            next_month = year_month.month + 1
            pre_year = year_month.year
            pre_month = year_month.month - 1

        next_year_month = str(next_year) + "-" + str(next_month)
        pre_year_month = str(pre_year) + "-" + str(pre_month)


        # 현재 로그한 유저는 유저목록에서 제외시켜 출력하기 위해
        users = User.objects.exclude(id=request.user.id)
        # friend = Friend.objects.get(current_user=request.user) => need to create
        friend, created = Friend.objects.get_or_create(current_user=request.user)
        friends = friend.users.all()

        args = {
            'year_month': year_month,
            'next_year_month': next_year_month,
            'pre_year_month': pre_year_month,
            'title': title,
            'posts': posts,
            'users': users,
            'friends': friends,
        }
        return render(request, self.template_name, args)

    def post(self, request):
        return render(request, self.template_name)

# class FilterView(TemplateView):
#     template_name = 'album/home.html'
#
#     def get(self, request):
#         posts = Calendar.objects.order_by('-date')
#         calendar_filter = CalendarFilter(request.GET, queryset=posts)
#
#         # 현재 로그한 유저는 유저목록에서 제외시켜 출력하기 위해
#         users = User.objects.all()
#         # friend = Friend.objects.get(current_user=request.user) => need to create
#         friend, created = Friend.objects.get_or_create(current_user=request.user)
#         friends = friend.users.all()
#
#         args = {
#             'users': users,
#             'friends': friends,
#             'filter': calendar_filter,
#         }
#         return render(request, self.template_name, args)
#
#     def post(self, request):
#         return render(request, self.template_name)



@login_required
def post_new(request):
    if request.method == 'POST':
        form = CalendarForm(request.POST, request.FILES)
        if form.is_valid():
            ###
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            date = form.cleaned_data['date']
            image = form.cleaned_data['image']

            Calendar.objects.create(
                author=request.user,
                title=title,
                description=description,
                date=date,
                image=image,
            ).save()

            return redirect('album:home')

    else:
        form = CalendarForm()

    args = {'form': form,}
    return render(request, 'album/calendar_new.html', args)

# 이미지 업로드 작업하기전 백업..
# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = CalendarForm(request.POST)
#         if form.is_valid():
#             ###
#             title = form.cleaned_data['title']
#             description = form.cleaned_data['description']
#             date = form.cleaned_data['date']
#             image = form.cleaned_data['image']
#
#             Calendar.objects.create(
#                 author=request.user,
#                 title=title,
#                 description=description,
#                 date=date,
#                 image=image,
#             ).save()
#
#             return redirect('album:home')
#
#     else:
#         form = CalendarForm()
#
#     args = {'form': form,}
#     return render(request, 'album/calendar_new.html', args)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Calendar, pk=pk)
    if request.method == "POST":
        form = CalendarForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('album:post_detail', pk=post.pk)
    else:
        form = CalendarForm(instance=post)
    return render(request, 'album/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Calendar, pk=pk)
    post.delete()
    return redirect('album:home')

class PostDetailView(TemplateView):
    template_name = 'album/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Calendar, pk=pk)
        form = CommentForm()
        users = User.objects.all()

        args = {'form': form, 'post': post, 'users': users}
        return render(request, self.template_name, args)

    def post(self, request, pk):
        post_pk = get_object_or_404(Calendar, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post_pk
            comment.save()
            text = form.cleaned_data['comment'] # forms의 post와 같음
            form = CommentForm() # 입력후 다시 빈칸으로 만들기
            return redirect('album:post_detail', pk=post_pk.pk)

        args =  {'form': form, 'text': text, 'post': post_pk}
        return render(request, self.template_name, args)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('album:post_detail', pk=comment.post.pk)

@login_required
def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)
    return redirect('accounts:view_profile_with_pk', pk=new_friend.pk)
