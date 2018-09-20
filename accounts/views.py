from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import User
from .models import UserProfile
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    # EntryForm,
    RegistrationForm,
    EditProfileForm,
    UserProfileImageForm
)

def index(request):
    return render(request, 'index.html')


def view_profile(request, pk=None):
    if pk:
        user_pk = User.objects.get(pk=pk)
    else:
        user_pk = request.user
    args = {'user': user_pk,}
    return render(request, 'accounts/profile.html', args)


def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, instance=request.user)
        user_profile_image_form = UserProfileImageForm(request.POST, request.FILES, instance=user_profile)

        if edit_profile_form.is_valid() and user_profile_image_form.is_valid():
            user = edit_profile_form.save()
            image = user_profile_image_form.save(commit=False)
            image.user = user

            if 'image' in request.FILES:

                image.image = request.FILES['image']

            image.save()
            return redirect(reverse('accounts:view_profile'))

        else:
            print(edit_profile_form.errors, user_profile_image_form.errors)
    else:
        edit_profile_form = EditProfileForm(instance=request.user)
        user_profile_image_form = UserProfileImageForm(instance=user_profile)

    args = {'edit_profile_form': edit_profile_form, 'user_profile_image_form': user_profile_image_form}
    return render(request, 'accounts/edit_profile.html', args)


#
# def home(request):
#     entries = Entry.objects.all() # 모든 게시물 출력
#     # entries = Entry.objects.filter(author=request.user) # 본인 게시물만 출력
#     args = {'entries': entries,}
#     return render(request, 'calendar/home.html', args)
#
# def details(request, pk):
#     entry = get_object_or_404(Entry, pk=pk)
#     args = {'entry': entry,}
#     return render(request, 'calendar/details.html', args)
#
# def add(request):
#     if request.method == 'POST':
#         form = EntryForm(request.POST)
#         if form.is_valid():
#             ###
#             name = form.cleaned_data['name']
#             date = form.cleaned_data['date']
#             description = form.cleaned_data['description']
#
#             Entry.objects.create(
#                 author=request.user,
#                 name=name,
#                 date=date,
#                 description=description,
#             ).save()
#
#             return HttpResponseRedirect('/')
#
#     else:
#         form = EntryForm()
#
#     args = {'form': form,}
#     return render(request, 'calendar/form.html', args)
#
# def delete(request, pk):
#     if request.method == 'DELETE':
#         entry = get_object_or_404(Entry, pk=pk)
#         entry.delete()
#
#     return HttpResponseRedirect('/')

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            ######### this makes users automatically log in when they successfully register
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            ##########
            return redirect(reverse('home'))
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'registration/reg_form.html', args)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Password has been successfully changed.")
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
    else:
        form = PasswordChangeForm(user=request.user)

    args = {'form': form}
    return render(request, 'accounts/change_password.html', args)
