from rest_framework import serializers
from django.contrib.auth import get_user_model  # Стандартты User орнына осыны ал
from .models import Post, Media, Comment, Like, Follow, SavedPost

User = get_user_model()  # Қазіргі активті User моделін анықтайды
# 1. Қолданушы сериализаторы
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Қажетті өрістерді қос: bio немесе avatar_url тек сенің моделіңде болса ғана жұмыс істейді
        fields = ['id', 'username', 'email']

# 2. Медиа (Сурет/Видео)
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'post', 'file', 'is_video']

# 3. Посттар (ЕҢ МАҢЫЗДЫСЫ: Лайктар мен Медиа осында)
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    media = MediaSerializer(many=True, read_only=True)
    
    # Лайктар санын есептейтін жаңа өрістер
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
        # Постқа қанша адам лайк басқанын есептейді
        return obj.likes.count() if hasattr(obj, 'likes') else obj.like_set.count()

    def get_is_liked(self, obj):
        # Қазіргі кіріп тұрған юзер лайк басты ма, жоқ па (True/False)
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
        fields = ['id', 'follower', 'followee'] # Моделіңде 'following' немесе 'followee' екенін тексер

# 7. Сақталғандар
class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post']