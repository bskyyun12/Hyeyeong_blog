from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import User
from .models import UserProfile
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from album.models import Friend
from django.contrib.auth.decorators import login_required
from .forms import (
    # EntryForm,
    RegistrationForm,
    EditProfileForm,
    UserProfileImageForm
)

def welcome(request):
    return render(request, 'welcome.html')

@login_required
def view_profile(request, pk=None):
    if pk:
        user_pk = User.objects.get(pk=pk)
    else:
        user_pk = request.user

    friend, created = Friend.objects.get_or_create(current_user=request.user)
    friends = friend.users.all()

    args = {
        'user': user_pk,
        'friends': friends,
    }
    return render(request, 'accounts/profile.html', args)

@login_required
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
            return redirect(reverse('album:home'))
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'registration/reg_form.html', args)

@login_required
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
