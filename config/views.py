from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import  Post, Comment, Like, Follow, SavedPost, Media
from .serializers import *
from .permissions import IsOwnerOrReadOnly

# --- 1. AUTH & REGISTRATION ---
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({"error": "Username және Password міндетті!"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Бұл username бос емес!"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# --- 2. USERS CRUD ---
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOwnerOrReadOnly])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method in ['PUT', 'DELETE'] and request.user.id != user.id:
        return Response({"detail": "Бұл сенің профилің емес!"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- 3. POSTS CRUD ---
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOwnerOrReadOnly])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method in ['PUT', 'DELETE'] and post.author != request.user:
        return Response({"detail": "Бұл сенің постың емес!"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- 4. COMMENTS ---
# --- 4. COMMENTS ---
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ЖАҢА: Пікірді көру және ӨЗГЕРТУ (PUT)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({"error": "Пікір табылмады"}, status=status.HTTP_404_NOT_FOUND)

    # Өзгерту немесе өшіру үшін автор екенін тексеру
    if request.method in ['PUT', 'DELETE'] and comment.author != request.user:
        return Response({"detail": "Бұл сенің пікірің емес!"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({"message": "Пікір өшірілді"}, status=status.HTTP_204_NO_CONTENT)

# --- 5. LIKES (Істеп тұр ма?) ---
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def like_toggle(request, post_id):
    # Тексеру: мұндай пост бар ма?
    if not Post.objects.filter(id=post_id).exists():
        return Response({"error": "Мұндай пост жоқ!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # get_or_create — егер лайк болса, соны алады, болмаса жаңасын жасайды
        like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
        if not created:
            return Response({"message": "Лайк бұрыннан бар"}, status=status.HTTP_200_OK)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        deleted_count, _ = Like.objects.filter(user=request.user, post_id=post_id).delete()
        if deleted_count == 0:
            return Response({"message": "Лайк табылмады"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Unliked"}, status=status.HTTP_204_NO_CONTENT)
# --- 6. FOLLOW SYSTEM ---
# --- 6. FOLLOW SYSTEM ---
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def follow_user(request, pk):
    try:
        # User = get_user_model() арқылы алынған нысан екеніне сенімді бол
        target_user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "Қолданушы табылмады"}, status=status.HTTP_404_NOT_FOUND)

    # 1. GET: Жазылу статусын тексеру
    if request.method == 'GET':
        follow = Follow.objects.filter(follower=request.user, followee=target_user).first()
        if follow:
            serializer = FollowSerializer(follow)
            return Response({"following": True, "data": serializer.data})
        # 404 емес, 200 қайтарған дұрыс, өйткені бұл қате емес, жай ғана статус
        return Response({"following": False}, status=status.HTTP_200_OK)

    # 2. POST: Жазылу
    elif request.method == 'POST':
        if request.user == target_user:
            return Response({"error": "Өзіңе жазыла алмайсың!"}, status=status.HTTP_400_BAD_REQUEST)
        
        # get_or_create дубляж жасамайды, өте дұрыс таңдау
        follow, created = Follow.objects.get_or_create(follower=request.user, followee=target_user)
        
        if created:
            return Response({"message": "Сен жазылдың", "following": True}, status=status.HTTP_201_CREATED)
        return Response({"message": "Сен бұрыннан жазылғансың"}, status=status.HTTP_200_OK)

    # 3. DELETE: Жазылудан шығу (Unfollow)
    elif request.method == 'DELETE':
        # delete() жасалғанда неше объект өшкенін қайтарады
        deleted_count, _ = Follow.objects.filter(follower=request.user, followee=target_user).delete()
        
        if deleted_count > 0:
            return Response({"message": "Жазылу тоқтатылды", "following": False}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Сен бұл адамға жазылмағансың"}, status=status.HTTP_400_BAD_REQUEST)
# --- 7. SAVED POSTS ---

# Бұл функция барлық сақталған посттарды тізім қылып қайтарады
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saved_posts_list(request):
    saved = SavedPost.objects.filter(user=request.user)
    serializer = SavedPostSerializer(saved, many=True)
    return Response(serializer.data)

# Бұл функция нақты бір постты сақтайды немесе өшіреді
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def saved_post_detail(request, pk):
    if request.method == 'GET':
        saved = SavedPost.objects.filter(user=request.user, post_id=pk).first()
        if saved:
            serializer = SavedPostSerializer(saved)
            return Response(serializer.data)
        return Response({"saved": False}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        SavedPost.objects.get_or_create(user=request.user, post_id=pk)
        return Response({"message": "Пост сақталды"}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        SavedPost.objects.filter(user=request.user, post_id=pk).delete()
        return Response({"message": "Сақталғандардан өшірілді"}, status=status.HTTP_204_NO_CONTENT)
# 8.1. Жаңа медиа жүктеу
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def media_upload(request):
    serializer = MediaSerializer(data=request.data)
    if serializer.is_valid():
        # Тексеру: юзер өз постына медиа қосып жатыр ма?
        post = serializer.validated_data.get('post')
        if post.author != request.user:
            return Response({"detail": "Сен басқа біреудің постына сурет қоса алмайсың!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 8.2. Медианы өзгерту және өшіру (ID арқылы)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def media_detail(request, pk):
    try:
        media = Media.objects.get(pk=pk)
    except Media.DoesNotExist:
        return Response({"error": "Медиа табылмады"}, status=status.HTTP_404_NOT_FOUND)

    # Авторды тексеру
    if media.post.author != request.user:
        return Response({"detail": "Бұл сенің медиа-файлың емес!"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = MediaSerializer(media)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MediaSerializer(media, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        media.delete()
        return Response({"message": "Файл сәтті өшірілді"}, status=status.HTTP_204_NO_CONTENT)