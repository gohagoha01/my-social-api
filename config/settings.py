import os
from pathlib import Path
from datetime import timedelta

# Негізгі жолдар
BASE_DIR = Path(__file__).resolve().parent.parent

# Локальді жұмыс үшін DEBUG әрқашан True
DEBUG = True

SECRET_KEY = 'django-insecure-local-only-key-12345'

# Телефоның мен компьютеріңнің IP адрестеріне рұқсат
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.166.1', '*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # СЕРІКТЕС КІТАПХАНАЛАР
    'rest_framework',
    'rest_framework_simplejwt',
    
    # СЕНІҢ ҚОСЫМШАҢ
    'config', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ДЕРЕКТЕР ҚОРЫ (ТЕК SQLITE)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# СЕНІҢ USER МОДЕЛІҢ
AUTH_USER_MODEL = 'config.User'

# REST FRAMEWORK ЖӘНЕ JWT БАПТАУЛАРЫ
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ТЕСТЕР ҮШІН ПАРОЛЬ ТЕКСЕРГІШТЕРДІ ӨШІРУГЕ БОЛАДЫ
AUTH_PASSWORD_VALIDATORS = []

# УАҚЫТ ЖӘНЕ ТІЛ
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

# СТАТИКАЛЫҚ ЖӘНЕ МЕДИА ФАЙЛДАР
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'