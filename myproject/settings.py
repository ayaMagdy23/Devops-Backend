# from decouple import config
# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# # Quick-start development settings - unsuitable for production
# SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool)
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# # Load OpenAI API key from environment variables
# load_dotenv()
# OPENAI_API_KEY = config('OPENAI_API_KEY')

# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'rest_framework_api_key',
#     'rest_framework.authtoken',
#     'myapps',
#     'corsheaders'
# ]

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_api_key.authentication.APIKeyAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }


# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # CORS configuration
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
# ]

# ROOT_URLCONF = 'myproject.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'myproject.wsgi.application'

# # Database configuration (PostgreSQL 15)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',  # Change this to your database name in pgAdmin
#         'USER': 'postgres',  # Your PostgreSQL username
#         'PASSWORD': 'ayagedoteta',  # The password you set for PostgreSQL
#         'HOST': 'localhost',  # Keep this if PostgreSQL is running locally
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files
# STATIC_URL = '/static/'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from decouple import config
import os
from pathlib import Path
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# External API Keys
SUPABASE_URL = 'https://xivukiickdgkworwjums.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhpdnVraWlja2Rna3dvcndqdW1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMxOTM2MjIsImV4cCI6MjA1ODc2OTYyMn0.flnVDYNOYkz67aVRxuR-rw_Tcgb1BmduuEoeZ1fZTCE'

# Security settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Ensure this path is correct
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# OpenAI API Key (if needed)
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
    'rest_framework_simplejwt',  # If you're using JWT for authentication
    'rest_framework',  # If you're using DRF
    'corsheaders',     # If you're using CORS

    'myapps',  # Your custom app
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]




# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# Middleware
MIDDLEWARE = [
     'corsheaders.middleware.CorsMiddleware',  # Ensure CORS middleware is above CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
   
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (for development)

CORS_ALLOW_CREDENTIALS = True  # Allow cookies (including CSRF)

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://192.168.56.1:3000",  # Your frontend's IP
]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False  # Set to True if using HTTPS
CSRF_USE_SESSIONS = True

# URL Configuration
ROOT_URLCONF = 'myproject.urls'

# Templates settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'myproject.wsgi.application'

# Database configuration (Using dj_database_url for flexibility)
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in the database
