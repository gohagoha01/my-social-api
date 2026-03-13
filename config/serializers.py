from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Media, Comment, Like, Follow, SavedPost, Story, StoryLike, StoryReply, Note 

User = get_user_model()

# 1. Қолданушы сериализаторы
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 2. Медиа (Сурет/Видео)
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'post', 'file', 'is_video']

# 3. Посттар
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    media = MediaSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username', 'caption', 
            'created_at', 'media', 'likes_count', 'is_liked'
        ]
        read_only_fields = ['author']

    def get_likes_count(self, obj):
        return obj.likes.count() if hasattr(obj, 'likes') else obj.like_set.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists() if hasattr(obj, 'likes') else obj.like_set.filter(user=request.user).exists()
        return False

# 4. Комментарийлер
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'text', 'created_at']
        read_only_fields = ['author']

# 5. Лайктар
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']

# 6. Жазылу (Follows)
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee']

# 7. Сақталғандар
class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post']

# --- ЖАҢА ҚОСЫЛҒАН СТОРИЗ СЕРИАЛИЗАТОРЛАРЫ ---

# 8. Сториз Лайк
class StoryLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryLike
        fields = ['id', 'user', 'story']
        read_only_fields = ['user']

# 9. Сториз Жауап (Reply)
class StoryReplySerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = StoryReply
        fields = ['id', 'story', 'user', 'username', 'text', 'created_at']
        read_only_fields = ['user']

# 10. Сториз (Басты сериализатор)
class StorySerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()
    replies = StoryReplySerializer(many=True, read_only=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Story
        fields = [
            'id', 'user', 'author_username', 'file', 
            'is_video', 'created_at', 'is_active', 
            'likes_count', 'replies'
        ]
        read_only_fields = ['user']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
class NoteSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar_url', read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'user', 'username', 'avatar', 'text', 'location', 'created_at', 'is_active']
        read_only_fields = ['user']