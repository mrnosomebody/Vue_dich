from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserProfileForm
from .models import *
from .utilities import create_notification


def frontpage(request):
    posts = Post.objects.all()
    for post in posts:
        likes = post.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            post.liked = True
        else:
            post.liked = False

    return render(request, 'core/frontpage.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('frontpage')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def feed(request):
    userids = [request.user.id]
    posts = Post.objects.filter(created_by_id__in=userids)
    return render(request, 'feed/feed.html', {'posts': posts})

def search(request):
    query = request.GET.get('query','')

    if len(query) >0 :
        posters = User.objects.filter(username__icontains=query)
        posts = Post.objects.filter(body__icontains=query)
    else:
        posters = []
        posts = []

    context = {
        'posters':posters,
        'query':query,
        'posts':posts
    }
    return render(request,'feed/search.html',context)

@login_required
def profile(request,username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()

    for post in posts:
        likes = post.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            post.liked = True
        else:
            post.liked = False

    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'core/profile.html', context)

@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.FOLLOWER:
            return redirect('profile', username=notification.created_by.username)
        elif notification.notification_type == Notification.LIKE:
            return redirect('profile', username=notification.to_user.username)

    return render(request, 'core/notifications.html')

@login_required
def follow(request, username):
    user = get_object_or_404(User, username=username)
    request.user.profile.follows.add(user.profile)
    create_notification(request, user, 'follower')
    return redirect('profile', username=username)

@login_required
def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    request.user.profile.follows.remove(user.profile)
    return redirect('profile', username=username)

def followers(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'core/followers.html', {'user': user})

def follows(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'core/follows.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile',username = request.user.username)
    else:
        form = UserProfileForm(instance=request.user.profile)
    context = {
        'user':request.user,
        'form':form
    }
    return render(request,'core/edit_profile.html',context)


@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.FOLLOWER:
            return redirect('profile', username=notification.created_by.username)
        elif notification.notification_type == Notification.LIKE:
            return redirect('profile', username=notification.to_user.username)

    return render(request, 'core/notifications.html')

