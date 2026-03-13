from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- AUTH & REGISTER ---
    path('api/register/', views.register_user),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- USERS & FOLLOW ---
    path('api/users/', views.user_list),
    path('api/users/<int:pk>/', views.user_detail),
    path('api/users/<int:pk>/follow/', views.follow_user),
    
    # --- POSTS ---
    path('api/posts/', views.post_list_create),
    path('api/posts/<int:pk>/', views.post_detail),
    path('api/posts/<int:post_id>/like/', views.like_toggle),

    # --- STORIES (ЖАҢА) ---
    path('api/stories/', views.story_list_create, name='story-list'),
    path('api/stories/<int:pk>/like/', views.story_like_toggle, name='story-like'),
    path('api/stories/<int:pk>/reply/', views.story_reply_create, name='story-reply'),
    path('api/stories/<int:pk>/delete/', views.story_delete, name='story-delete'),

    path('api/notes/', views.note_list_create, name='notes'),
    
    # --- SAVED POSTS ---
    path('api/saved/', views.saved_posts_list), 
    path('api/posts/<int:pk>/save/', views.saved_post_detail),

    # --- COMMENTS ---
    path('api/comments/', views.comment_list_create),
    path('api/comments/<int:pk>/', views.comment_detail),
    
    # --- MEDIA ---
    path('api/media/upload/', views.media_upload),
    path('api/media/<int:pk>/', views.media_detail),
]

# Медиа файлдарды (сурет/видео) даму кезеңінде көрсету үшін
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)