from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

# 1. User моделі
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

# 3. Медиа
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='post_media/')
    is_video = models.BooleanField(default=False) 

# 4. Комментарийлер
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 5. Лайктар
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

# 7. Сақталғандар
class SavedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# --- STORIES SECTION ---

# 8. Сториз (24 сағаттық посттар)
class Story(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    file = models.FileField(upload_to='stories/')
    is_video = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Story by {self.user.username} at {self.created_at}"

    @property
    def is_active(self):
        return timezone.now() < self.created_at + timedelta(hours=24)

# 9. Сторизге лайк басу
class StoryLike(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('story', 'user')

# реклама
class Advertisement(models.Model):
    title = models.CharField(max_length=255, verbose_name="Тақырыбы")
    image = models.ImageField(upload_to='ads/', verbose_name="Суреті")
    description = models.TextField(verbose_name="Сипаттамасы")
    link = models.URLField(verbose_name="Сілтеме (URL)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Жарнама"
        verbose_name_plural = "Жарнамалар"

    def __str__(self):
        return self.title        

# 10. Сторизге жауап жазу (Reply)
class StoryReply(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} to {self.story.id}"

# --- NEW: NOTES SECTION ---

# 11. Заметки (Notes - 60 символдық статус)
class Note(models.Model):
    # OneToOneField - әр юзерде тек 1 заметка болуы үшін
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note')
    text = models.CharField(max_length=60)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True) # auto_now заметка жаңарғанда уақытты өзгертеді

    def __str__(self):
        return f"Note by {self.user.username}: {self.text[:20]}"

    @property
    def is_active(self):
        # 24 сағаттық өмір сүру уақыты
        return timezone.now() < self.created_at + timedelta(hours=24)