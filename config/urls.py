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
    
    # AUTH & REGISTER
    path('api/register/', views.register_user),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # USERS & FOLLOW
    path('api/users/', views.user_list),
    path('api/users/<int:pk>/', views.user_detail),
    path('api/users/<int:pk>/follow/', views.follow_user),
    
    
   # --- POSTS & SAVED ---
path('api/posts/', views.post_list_create),
path('api/posts/<int:pk>/', views.post_detail),

# --- САҚТАЛҒАНДАР (Saved Posts) ---
path('api/saved/', views.saved_posts_list),           # Барлық сақталғандар тізімі (GET)
path('api/posts/<int:pk>/save/', views.saved_post_detail), #
    # COMMENTS
    path('api/comments/', views.comment_list_create),
path('api/comments/<int:pk>/', views.comment_detail),    
    # LIKES
    path('api/posts/<int:post_id>/like/', views.like_toggle),
    
    # MEDIA
    # 6. MEDIA (Суреттер/Видео)
    path('api/media/upload/', views.media_upload),       # POST (Жүктеу)
    path('api/media/<int:pk>/', views.media_detail),    # GET, PUT, DELETE (ID бойынша)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)