from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. User моделі (bio және avatar қосылған)
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

# 2. Посттар
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 3. Медиа (Бір постта бірнеше сурет болуы мүмкін)
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='post_media/')
    # Сурет пе әлде видео ма анықтау үшін
    is_video = models.BooleanField(default=False) 

# 4. Комментарийлер
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 5. Лайктар (UniqueConstraint арқылы бір адам бір постқа тек 1 лайк баса алады)
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

# 6. Подписки (Follows)
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followee')

# 7. Сақталғандар (Saved Posts)
class SavedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    