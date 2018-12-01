"""
Django settings for market project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=7r3=0s4p%3(5_vlrk4$tx#i$_00=o0jg$6awfzj@et_)$@&gq'

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
    'person.apps.PersonConfig',  # 用户
    'goods.apps.GoodsConfig',  # 商品
    'cart.apps.CartConfig',  # 购物车
    'order.apps.OrderConfig',  # 订单
    'ckeditor',  # 添加ckeditor富文本编辑器
    'ckeditor_uploader',  # 添加ckeditor富文本编辑器文件上传部件
    'haystack',  # 全文检索框架
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

ROOT_URLCONF = 'market.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },

]

WSGI_APPLICATION = 'market.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# 设置静态文件根目录  上线的时候使用
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# redis 的配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# session配置
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# 短信服务配置
ACCESS_KEY_ID = "LTAI2qSiJdWP87em"
ACCESS_KEY_SECRET = "FzORQ587PgGBoOAdmxzCjaxQi8klUi"

MEDIA_URL = "/static/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')

# 设置ckeditor的上传目录
CKEDITOR_UPLOAD_PATH = "uploads/"

# 编辑器样式配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}


# # 全文检索框架的配置
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         # 配置搜索引擎
#         'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
#         # 配置索引文件目录
#         'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
#     },
# }

# 全文检索框架的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 配置搜索引擎
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 中文分词 使用jieba的whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 配置索引文件目录
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

#当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10


# # 七牛云密钥等配置
# QINIU_ACCESS_KEY = 'EO6_JKAYMuwttDgG8yj4jmsYDBg1zGXJr07s95YH'
# QINIU_SECRET_KEY = 'ul6OeTdFdTEikUumen1jwvbtzmxl1ljFA_M6cQD2'
# QINIU_BUCKET_NAME = 'market'
# QINIU_BUCKET_DOMAIN = 'pj1vf3xt8.bkt.clouddn.com/'
# QINIU_SECURE_URL = False      #使用https
# PREFIX_URL = 'http://'
#
# # 上传文件地址配置
# MEDIA_URL = PREFIX_URL + QINIU_BUCKET_DOMAIN + "/"
# # 上传文件的存储引擎配置
# DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'
#
# # 静态文件的url配置
# STATIC_URL = QINIU_BUCKET_DOMAIN + '/static/'
# # 静态文件的存储引擎
# STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'