"""
Django settings for learnifyApi project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from django.conf import settings
import os
from decouple import config
from firebase_admin import initialize_app

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # packages
    'rest_framework',
    'rest_framework_simplejwt',
    'djmoney',
    'social_django',  # django social auth
     "debug_toolbar",
     'django_filters',
     'sslserver',
     "corsheaders",
     "fcm_django",
    #  'paystack',

    # local apps
    'account',
    'courses',
    'user_profile',
    'my_subscription',
    'payment',
    'notification',
 
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.TestMiddleWare',
]

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING':False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
                                    #    'rest_framework.authentication.BasicAuthentication',
        ),
    
}

ROOT_URLCONF = 'learnifyApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates/"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'learnifyApi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS= [BASE_DIR / 'static/']

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL='account.CustomUser'



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_OBTAIN_SERIALIZER": "account.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

if DEBUG:
    MEDIA_URL="media/"
    MEDIA_ROOT=os.path.join(BASE_DIR,'media/')


SOCIAL_AUTH_FACEBOOK_KEY =config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET =config('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
            'fields': 'id,name,email',
            }
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

AUTHENTICATION_BACKENDS = (
        # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',

      # Google  OAuth2
    'social_core.backends.google.GoogleOAuth2',

     # GitHub OAuth2
    'social_core.backends.github.GithubOAuth2',

        # Instagram OAuth2
    'social_core.backends.instagram.InstagramOAuth2',
 
    'django.contrib.auth.backends.ModelBackend',
)

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

SOCIAL_AUTH_PIPELINE = [  # Note: Sequence of functions matters here.
    'social_core.pipeline.social_auth.social_details',  # 0
    'social_core.pipeline.social_auth.social_uid',  # 1
    'social_core.pipeline.social_auth.auth_allowed',  # 2
    'social_core.pipeline.social_auth.social_user',  # 3
    'social_core.pipeline.user.get_username',  # 4
    # 'social_core.pipeline.social_auth.associate_by_email',  # 5
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',  # 6
    'social_core.pipeline.social_auth.load_extra_data',  # 7
    'social_core.pipeline.user.user_details',  # 8
]

SOCIAL_AUTH_JSONFIELD_ENABLED = True


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST ='smtp.gmail.com'
EMAIL_HOST_USER =config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


PAYSTACK_SECRET_KEY=config("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY=config("PAYSTACK_PUBLIC_KEY")


STRIP_SECRET_KEY=config("STRIP_SECRET_KEY")
STRIP_PUBLISH_KEY=config("STRIP_PUBLISH_KEY")


CORS_ALLOWED_ORIGINS = ["http://localhost:8000",
                        "http://127.0.0.1:8000",
                        "https://26e9-197-211-58-197.ngrok-free.app"]
CORS_ALLOW_ALL_ORIGINS=True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "https://26e9-197-211-58-197.ngrok-free.app",
]
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)


FIREBASE_APP=initialize_app()

FCM_DJANG0_SETTINGS={
    "DEFAULT_FIREBASE_APP":None,
    "ONE_DEVICE_PER_USER":False,
    "DELETE_INACTIVE_DEVICES":False
}


DOMIN=config("DEFAULT_DOMIN")
PROTOCOL=config("PROTOCOL")


# STATIC_ROOT = BASE_DIR / "staticfiles"

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME':env('CLOUDINARY_CLOUD_NAME'),
#     'API_KEY':env('CLOUDINARY_API_KEY'),
#     'API_SECRET':env('CLOUDINARY_API_SECRET')
# }


#    MEDIA_URL="/media/"
#     DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# DATABASES = {
#             'default': dj_database_url.parse(env('DATABASE_URL'))
#         }