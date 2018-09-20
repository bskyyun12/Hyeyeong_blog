from django.shortcuts import render, redirect, get_object_or_404
from .models import Calendar, Comment
from accounts.models import User
from django.utils import timezone
from django.views.generic import TemplateView
from .filters import CalendarFilter
from .forms import (
    CalendarForm,
    CommentForm
)

# def search(request):
#     post_list = Calendar.objects.all()
#     calendar_filter = CalendarFilter(request.GET, queryset=post_list)
#     return render(request, 'album/calendar_list.html', {'filter': calendar_filter})

class FilterView(TemplateView):
    template_name = 'album/home.html'

    def get(self, request):
        posts = Calendar.objects.order_by('-date')
        calendar_filter = CalendarFilter(request.GET, queryset=posts)
        args = {
            'filter': calendar_filter,
        }
        return render(request, self.template_name, args)

    def post(self, request):
        return render(request, self.template_name)


# class CalendarView(TemplateView):
#     template_name = 'album/home.html'
#
#     def get(self, request):
#         posts = Calendar.objects.order_by('-date')
#         args = {
#             'posts': posts,
#         }
#         return render(request, self.template_name, args)
#
#     def post(self, request):
#         return render(request, self.template_name)

def post_new(request):
    if request.method == 'POST':
        form = CalendarForm(request.POST)
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


def post_edit(request, pk):
    post = get_object_or_404(Calendar, pk=pk)
    if request.method == "POST":
        form = CalendarForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('album:post_detail', pk=post.pk)
    else:
        form = CalendarForm(instance=post)
    return render(request, 'album/post_edit.html', {'form': form})

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


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('album:post_detail', pk=comment.post.pk)
