from pathlib import Path
import os
# from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "_jn6(j0+mu)a*dx*0n5^djms=uy5unlh4#o4%+-!5^#5!u(zqh"
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',  
    'users',
    'cart',
    'product',
    'payment',
    'order',
    'stripe',
    'blog',
    "debug_toolbar",
    "tailwind",
    "Molla",
    
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'mollo_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"mollo_backend/Templates"],
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

WSGI_APPLICATION = 'mollo_backend.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [
    BASE_DIR / 'mollo_backend' / 'static'
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STRIPE_SECRET_KEY='sk_test_51Pw4qzEnQNLsnCj1NLNJftCJaYhNo7ZYB2YntOJsO4OlQsscEdmZSCTRPlqBnnkFTKbs94g0bWQMXBsnizBzXdhh00lvuKtAqu'
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

#We are setting jezzmin and tailwind onto our porjet to customize the django defult admin dashboard 

JAZZMIN_SETTINGS = {
    "site_title": "MOlla Inventory Admin",
    "site_header": "Molla Admin",
    "welcome_sign": "Welcome to the Admin Dashboard",
    "show_sidebar": True,

}

TAILWIND_APP_NAME = 'Molla'
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

