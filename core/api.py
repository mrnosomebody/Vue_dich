import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from core.models import Post, Like
from .utilities import *


@login_required
def api_add_post(request):
    data = json.loads(request.body)
    body = data['body']

    post = Post.objects.create(body=body, created_by=request.user)
    return JsonResponse({'succes':True})

@login_required
def api_add_like(request):
    data = json.loads(request.body)
    post_id = data['post_id']
    if not Like.objects.filter(post_id=post_id).filter(created_by=request.user).exists():
        like = Like.objects.create(post_id=post_id, created_by=request.user)
        post = Post.objects.get(pk=post_id)
        create_notification(request,post.created_by,'like')

    return JsonResponse({'succes':True})