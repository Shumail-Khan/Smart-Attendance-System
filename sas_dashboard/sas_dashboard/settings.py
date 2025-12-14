import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

# ----------------------------------------------------------------------
# Installed Apps
# ----------------------------------------------------------------------
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "channels",
    'tailwind',
    'theme',

    # Local Apps
    "apps.core",
    "apps.persons",
    "apps.cameras",
    "apps.attendance",
    "apps.monitoring",
    "apps.reports",
    "apps.accounts",
]
if DEBUG:
    # Add django_browser_reload only in DEBUG mode
    INSTALLED_APPS += ["django_browser_reload"]

# ----------------------------------------------------------------------
# Middleware
# ----------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
if DEBUG:
    # Add django_browser_reload middleware only in DEBUG mode
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]
# ----------------------------------------------------------------------
# Root URLs and WSGI/ASGI
# ----------------------------------------------------------------------
ROOT_URLCONF = "sas_dashboard.urls"

WSGI_APPLICATION = "sas_dashboard.wsgi.application"
ASGI_APPLICATION = "sas_dashboard.asgi.application"

# ----------------------------------------------------------------------
# Database
# ----------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "db_sas"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # optional custom templates folder
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


# ----------------------------------------------------------------------
# DRF standard config (clean)
# ----------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ----------------------------------------------------------------------
# Static/Media
# ----------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] # for development
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------------------------------------------------
# CORS
# ----------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# ----------------------------------------------------------------------
# Channels & Redis
# ----------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
        # For production:
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}

# ----------------------------------------------------------------------
# AI Backend URL
# ----------------------------------------------------------------------
AI_BACKEND_URL = "http://localhost:8000/api"
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']
