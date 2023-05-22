"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ
import dj_database_url  # Deployment
from corsheaders.defaults import default_headers


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# env 파일로 이동! 감춰야해서!
# SECRET_KEY는 꼭 프로젝트 생성했을때 다른곳 복사가 아니라 setting에 있는것으로 해야함

SECRET_KEY = env("SECRET_KEY")
# GH_SECRET = env("GH_SECRET")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "RENDER" not in os.environ  # Deployment

# Deployment
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition


# 기본적으로 장고와 함께 설치되는것들
SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# 우리가 설치하는것들
CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "experiences.apps.ExperiencesConfig",
    "categories.apps.CategoriesConfig",
    "photos.apps.PhotosConfig",
    "wishlists.apps.WishlistsConfig",
    "reviews.apps.ReviewsConfig",
    "common.apps.CommonConfig",
    # "products.apps.ProductsConfig",
    # "coupons.apps.CouponsConfig",
    # "settingsOption.apps.SettingsoptionConfig",
    # "feedbacks.apps.FeedbacksConfig",
    # "chatrooms.apps.ChatroomsConfig",
    # "direct_messages.apps.DirectMessagesConfig",
    # "orders.apps.OrdersConfig",
    # "soldProducts.apps.SoldproductsConfig",
    # "carts.apps.CartsConfig",
    # "orderHistory.apps.OrderhistoryConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "corsheaders",  # cors
]


INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

# 유저사용하기위해 적어줘야함 장고문서에있음
AUTH_USER_MODEL = "users.User"

MEDIA_ROOT = "uploads"  # upload 폴더안에 미디어나 사진이 저장될것임

MEDIA_URL = "user-uploads/"  # 이이름으로 사진이나 영상에 접근 가능할것임 / 로 끝나야함

PAGE_SIZE = 3

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # 이게 맨처음 쓰던 기본
        "rest_framework.authentication.SessionAuthentication",
        # 이것이 가장구린 1번째
        # "config.authentication.TrustMeBroAuthentication",  # 유저인증.. view들보다 먼저 여기를 들린다 연습만함
        # 실제로는 장고 유저확인을 사용함
        #
        # 2번째 방법, 밑에 껄 사용하기위해서는 python migrate 해야함
        # "rest_framework.authentication.TokenAuthentication",
        #
        # 3번째 jwt -decode할때 필요함
        # "config.authentication.JWTAuthentication",
    ]
}


MIDDLEWARE = [
    # disableCSRFMiddleware setting안에 이거 파일 필수!!!!!!!! 없으면 애러 생김
    "config.disableCSRFMiddleware.DisableCSRFMiddleware",  # csrf 제거
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Deployment
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # cors
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",  # 프론트엔드에서 csrf가 보내지지 않는다...일단 꺼둠
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# Deployment
# 디버그가 켜져있으면 개발떄 썼던 sqlite3을 쓸것이고

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
        )
    }


# 안켜져있으면 postgre를 사용할것임
# 디비가 연결이 종료되기전 연결 유지시간


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"  # deployment 그냥 /만 앞에 추가함

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://blankhouse.netlify.app",
]

CORS_ALLOW_CREDENTIALS = True

# crsf토큰.. 포론트엔드 post를 믿을수없기에 믿게 만들어주고
# 프론트엔드에서 매번 axios에 포함시켜 post와 같이 보내야함
# 장고에서 기본적으로 crsf를 쿠키로 프론트에 보내 저장시킴
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://blankhouse.netlify.app",
]

# if CORS_ALLOW_ALL_ORIGINS and not CORS_ALLOW_CREDENTIALS:
#     response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"
# else:
#     response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin


# !!! HTTPONLY 가 true면 자바스크립트에서 쿠키가 안읽어진다

# CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOW_HEADERS = list(default_headers) + ["Set-Cookie"]
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = False
# # not debug = 배포버전이라는뜻
# if not DEBUG:
#     SESSION_COOKIE_DOMAIN = ".localhost"
#     CSRF_COOKIE_DOMAIN = ".localhost"


# file upload
# django < 4.2
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


AWS_STORAGE_BUCKET_NAME = "shoppingmallapp"

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
# AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
# AWS_S3_ACCESS_KEY_ID 그냥 root 로 사용하기로함
# AWS_S3_SECRET_ACCESS_KEY
