from pathlib import Path
from dotenv import load_dotenv 
from decouple import config
import os
import sys

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, 'books_app'))

# Import cloudinary config
from books_app.config import configure_cloudinary
configure_cloudinary()


"""
# Load environment variables from .env file
"""
load_dotenv(BASE_DIR / '.env') 


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-905*$z^mjb^6#zvq2=@+8efzsgqcah$g5pk(x76rc40sa&=fd='
SECRET_KEY = os.getenv('SECRET_KEY')

""" JWT Configuration - Get the secret from environment variables """
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not found in environment variables")

JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
if not JWT_ALGORITHM:
    raise ValueError("JWT_ALGORITHM not found in environment variables")

JWT_ACCESS_TOKEN_LIFETIME_HOURS = os.getenv('JWT_ACCESS_TOKEN_LIFETIME_HOURS')
if not JWT_ACCESS_TOKEN_LIFETIME_HOURS:
    raise ValueError("JWT_ACCESS_TOKEN_LIFETIME_HOURS not found in environment variables")


""" CLOUDINARY CONFIGURATION """

cloud_name = config('CLOUDINARY_CLOUD_NAME')
if not cloud_name:
    raise ValueError("CLOUDINARY_CLOUD_NAME not found in environment variables")

api_key = config('CLOUDINARY_API_KEY')
if not api_key:
    raise ValueError("CLOUDINARY_API_KEY not found in environment variables")

api_secret = config('CLOUDINARY_API_SECRET')
if not api_secret:
    raise ValueError("CLOUDINARY_API_SECRET not found in environment variables")

CLOUDINARY_URL = f"cloudinary://{api_key}:{api_secret}@{cloud_name}"

""" End of CLOUDINARY CONFIGURATION """


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Application
    'books_app.apps.BooksAppConfig',
    # cloudnary package
    'cloudinary',
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
