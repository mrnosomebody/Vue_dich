from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self',related_name='followed_by',symmetrical=False)
    avatar = models.ImageField(upload_to='uploads',default='kot.png')

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

class Post(models.Model):
    body = models.CharField(max_length=255)
    created_by = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created_at',)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    FOLLOWER = 'follower'
    LIKE = 'like'

    CHOICES=(
        (FOLLOWER,'Follower'),
        (LIKE, 'Like')
    )

    to_user = models.ForeignKey(User,related_name='notifications',on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20,choices=CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']