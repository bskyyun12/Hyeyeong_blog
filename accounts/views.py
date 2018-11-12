from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import User
from .models import UserProfile, BabyProfile
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from album.models import Calendar, Friend
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import (
    # EntryForm,
    RegistrationForm,
    EditProfileForm,
    UserProfileImageForm,
    BabyForm,
    MilestoneForm
)

def baby_profile(request):
    baby = BabyProfile.objects.get(first_name='Angelica Teresa Hyeyeong')
    today = datetime.now().date()

    posts = []
    newyear_post = Calendar.objects.filter(date__month='1', date__day='1').order_by('date').last()
    posts.append(newyear_post)

    christmas_post = Calendar.objects.filter(date__month='12', date__day='25').order_by('date').last()
    posts.append(christmas_post)

    if request.method == "POST":
        form = MilestoneForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            if 'image' in request.FILES:
                print('--------------milestone test-----------------')
            form.save()
            return redirect('accounts:baby_profile')
    else:
        form = MilestoneForm()

    args = {
        'baby': baby,
        'posts': posts,
        'today': today,
        'form': form,
    }
    return render(request, 'accounts/baby_profile.html', args)

@login_required
def edit_baby_profile(request):
    baby = get_object_or_404(BabyProfile, first_name='Angelica Teresa Hyeyeong')
    if request.user.is_superuser:
        if request.method == "POST":
            form = BabyForm(request.POST, instance=baby)
            if form.is_valid():
                baby = form.save(commit=False)
                if 'image' in request.FILES:
                    baby.image.delete()
                    baby.image = request.FILES['image']
                baby.save()
                return redirect('accounts:baby_profile')
        else:
            form = BabyForm(instance=baby)
        args = {
            'form': form,
        }
        return render(request, 'accounts/edit_baby_profile.html', args)
    else:
        return redirect('album:home')


def welcome(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            ######### this makes users automatically log in when they successfully register
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password1']
            # user = authenticate(email=email, password=password)
            # login(request, user)
            ##########
            return redirect(reverse('accounts:login'))
    else:
        form = RegistrationForm()


    args = {'form': form}
    return render(request, 'welcome.html', args)

def user_login(request):
    if request.method == 'GET':
        context = ''
        return render(request, 'registration/login.html', {'context': context})

    elif request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        # setting.py -> AUTHENTICATION_BACKENDS -> allow inactive users to login
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('album:home'))
            else:
                context = 'Your account is not activated yet. Please contact Gwangyeong to activate your account.'  # to display error?
                return render(request, 'registration/login.html', {'context': context})
        else:
            context = 'Please enter a correct email and password. Note that both fields may be case-sensitive.'   # to display error?
            return render(request, 'registration/login.html', {'context': context})

@login_required
def view_profile(request, pk=None):
    if pk:
        user_pk = User.objects.get(pk=pk)
    else:
        user_pk = request.user

    users = User.objects.exclude(id=request.user.id)
    # friend = Friend.objects.get(current_user=request.user) => need to create
    friend, created = Friend.objects.get_or_create(current_user=request.user)
    friends = friend.users.all()

    args = {
        'user': user_pk,
        'users': users,
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
