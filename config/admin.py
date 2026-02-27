from django.contrib import admin
from .models import User, Post, Media, Comment, Like, Follow, SavedPost

# 1. User (Пайдаланушылар)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# 2. Post (Посттар)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'caption', 'created_at')
    list_filter = ('created_at', 'author')

# 3. Media (Суреттер мен Видеолар)
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('post', 'is_video', 'file')

# 4. Comment (Пікірлер)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_at')

# 5. Like (Лайктар)
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')

# 6. Follow (Жазылушылар)
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followee')

# 7. SavedPost (Сақталғандар)
@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')