"""
Django settings for linkding webapp.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import json
import os
import shlex

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "kgq$h3@!!vbb6*nzfz(dbze=*)zsroqa8gvc0#1gx$3cd8z99^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "bookmarks.apps.BookmarksConfig",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "rest_framework",
    "rest_framework.authtoken",
    "huey.contrib.djhuey",
    "mozilla_django_oidc",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "bookmarks.middlewares.LinkdingMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "bookmarks.urls"

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
                "bookmarks.context_processors.toasts",
                "bookmarks.context_processors.app_version",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

WSGI_APPLICATION = "bookmarks.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Website context path.
LD_CONTEXT_PATH = os.getenv("LD_CONTEXT_PATH", "")

LOGIN_URL = "/" + LD_CONTEXT_PATH + "login"
LOGIN_REDIRECT_URL = "/" + LD_CONTEXT_PATH + "bookmarks"
LOGOUT_REDIRECT_URL = "/" + LD_CONTEXT_PATH + "login"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("TZ", "UTC")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/" + LD_CONTEXT_PATH + "static/"

# Collect static files in static folder
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# REST framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "bookmarks.api.auth.LinkdingTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

# Registration switch
ALLOW_REGISTRATION = False

# URL validation flag
LD_DISABLE_URL_VALIDATION = os.getenv("LD_DISABLE_URL_VALIDATION", False) in (
    True,
    "True",
    "true",
    "1",
)

# Background task enabled setting
LD_DISABLE_BACKGROUND_TASKS = os.getenv("LD_DISABLE_BACKGROUND_TASKS", False) in (
    True,
    "True",
    "true",
    "1",
)

# Huey task queue
HUEY = {
    "huey_class": "huey.SqliteHuey",
    "filename": os.path.join(BASE_DIR, "data", "tasks.sqlite3"),
    "immediate": False,
    "results": False,
    "store_none": False,
    "utc": True,
    "consumer": {
        "workers": 2,
        "worker_type": "thread",
        "initial_delay": 5,
        "backoff": 1.15,
        "max_delay": 10,
        "scheduler_interval": 10,
        "periodic": True,
        "check_worker_health": True,
        "health_check_interval": 10,
    },
}


# Enable OICD support if configured
LD_ENABLE_OIDC = os.getenv("LD_ENABLE_OIDC", False) in (True, "True", "true", "1")

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

if LD_ENABLE_OIDC:
    AUTHENTICATION_BACKENDS.append("mozilla_django_oidc.auth.OIDCAuthenticationBackend")

    OIDC_USERNAME_ALGO = "bookmarks.utils.generate_username"
    OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv("OIDC_OP_AUTHORIZATION_ENDPOINT")
    OIDC_OP_TOKEN_ENDPOINT = os.getenv("OIDC_OP_TOKEN_ENDPOINT")
    OIDC_OP_USER_ENDPOINT = os.getenv("OIDC_OP_USER_ENDPOINT")
    OIDC_OP_JWKS_ENDPOINT = os.getenv("OIDC_OP_JWKS_ENDPOINT")
    OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID")
    OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET")
    OIDC_RP_SIGN_ALGO = os.getenv("OIDC_RP_SIGN_ALGO", "RS256")
    OIDC_RP_SCOPES = os.getenv("OIDC_RP_SCOPES", "openid email profile")
    OIDC_USE_PKCE = os.getenv("OIDC_USE_PKCE", True) in (True, "True", "true", "1")
    OIDC_VERIFY_SSL = os.getenv("OIDC_VERIFY_SSL", True) in (True, "True", "true", "1")
    OIDC_USERNAME_CLAIM = os.getenv("OIDC_USERNAME_CLAIM", "email")

# Enable authentication proxy support if configured
LD_ENABLE_AUTH_PROXY = os.getenv("LD_ENABLE_AUTH_PROXY", False) in (
    True,
    "True",
    "true",
    "1",
)
LD_AUTH_PROXY_USERNAME_HEADER = os.getenv(
    "LD_AUTH_PROXY_USERNAME_HEADER", "REMOTE_USER"
)
LD_AUTH_PROXY_LOGOUT_URL = os.getenv("LD_AUTH_PROXY_LOGOUT_URL", None)

if LD_ENABLE_AUTH_PROXY:
    # Add middleware that automatically authenticates requests that have a known username
    # in the LD_AUTH_PROXY_USERNAME_HEADER request header
    MIDDLEWARE.append("bookmarks.middlewares.CustomRemoteUserMiddleware")
    # Configure auth backend that does not require a password credential
    AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.RemoteUserBackend"]
    # Configure logout URL
    if LD_AUTH_PROXY_LOGOUT_URL:
        LOGOUT_REDIRECT_URL = LD_AUTH_PROXY_LOGOUT_URL

# CSRF trusted origins
trusted_origins = os.getenv("LD_CSRF_TRUSTED_ORIGINS", "")
if trusted_origins:
    CSRF_TRUSTED_ORIGINS = trusted_origins.split(",")

# CORS
# https://pypi.org/project/django-cors-headers/
cors_enabled = False
cors_origins = os.getenv("LD_CORS_ALLOWED_ORIGINS", "")
if cors_origins:
    CORS_ALLOWED_ORIGINS = cors_origins.split(",")
    cors_enabled = True

cores_regex = os.getenv("LD_CORS_ALLOWED_REGEX", "")
if cores_regex:
    CORS_ALLOWED_ORIGIN_REGEXES = [cores_regex]
    cors_enabled = True

cors_all = os.getenv("LD_CORS_ALLOW_ALL", False) in (True, "True", "true", "1")
if cors_all:
    CORS_ALLOW_ALL_ORIGINS = True
    cors_enabled = True

if cors_enabled:
    MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
    CORS_ALLOW_CREDENTIALS = os.getenv("LD_CORS_ALLOW_CREDENTIALS", False) in (True, "True", "true", "1")
    CORS_URLS_REGEX = os.getenv("LD_CORS_URLS_REGEX", r"^/api/.*$")
    cors_methods = os.getenv("LD_CORS_ALLOWED_METHODS", "")
    if cors_methods:
        CORS_ALLOW_METHODS = cors_methods.split(",")
    CORS_ALLOW_HEADERS = os.getenv("LD_CORS_ALLOWED_HEADERS", "authorization,content-type").split(",")
    cors_expose_headers = os.getenv("LD_CORS_EXPOSE_HEADERS", "")
    if cors_expose_headers:
        CORS_EXPOSE_HEADERS = cors_expose_headers.split(",")
    cors_preflight_max_age = os.getenv("LD_CORS_PREFLIGHT_MAX_AGE")
    if cors_preflight_max_age:
        CORS_PREFLIGHT_MAX_AGE = int(cors_preflight_max_age)
    CORS_ALLOW_PRIVATE_NETWORK = os.getenv("LD_CORS_ALLOW_PRIVATE_NETWORK", False) in (True, "True", "true", "1")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

LD_DB_ENGINE = os.getenv("LD_DB_ENGINE", "sqlite")
LD_DB_HOST = os.getenv("LD_DB_HOST", "localhost")
LD_DB_DATABASE = os.getenv("LD_DB_DATABASE", "linkding")
LD_DB_USER = os.getenv("LD_DB_USER", "linkding")
LD_DB_PASSWORD = os.getenv("LD_DB_PASSWORD", None)
LD_DB_PORT = os.getenv("LD_DB_PORT", None)
LD_DB_OPTIONS = json.loads(os.getenv("LD_DB_OPTIONS") or "{}")

if LD_DB_ENGINE == "postgres":
    default_database = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": LD_DB_DATABASE,
        "USER": LD_DB_USER,
        "PASSWORD": LD_DB_PASSWORD,
        "HOST": LD_DB_HOST,
        "PORT": LD_DB_PORT,
        "OPTIONS": LD_DB_OPTIONS,
    }
else:
    default_database = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "data", "db.sqlite3"),
        "OPTIONS": LD_DB_OPTIONS,
        # Creating a connection loads the ICU extension into the SQLite
        # connection, and also loads an ICU collation. The latter causes a
        # memory leak, so try to counter that by making connections indefinitely
        # persistent.
        "CONN_MAX_AGE": None,
    }

DATABASES = {"default": default_database}

SQLITE_ICU_EXTENSION_PATH = "./libicu.so"
USE_SQLITE = default_database["ENGINE"] == "django.db.backends.sqlite3"
USE_SQLITE_ICU_EXTENSION = USE_SQLITE and os.path.exists(SQLITE_ICU_EXTENSION_PATH)

# Favicons
LD_DEFAULT_FAVICON_PROVIDER = "https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={url}&size=32"
LD_FAVICON_PROVIDER = os.getenv("LD_FAVICON_PROVIDER", LD_DEFAULT_FAVICON_PROVIDER)
LD_FAVICON_FOLDER = os.path.join(BASE_DIR, "data", "favicons")
LD_ENABLE_REFRESH_FAVICONS = os.getenv("LD_ENABLE_REFRESH_FAVICONS", True) in (
    True,
    "True",
    "true",
    "1",
)

# Previews settings
LD_PREVIEW_FOLDER = os.path.join(BASE_DIR, "data", "previews")
LD_PREVIEW_MAX_SIZE = int(os.getenv("LD_PREVIEW_MAX_SIZE", 5242880))
LD_PREVIEW_ALLOWED_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".webp",
]

# Asset / snapshot settings
LD_ASSET_FOLDER = os.path.join(BASE_DIR, "data", "assets")

LD_ENABLE_SNAPSHOTS = os.getenv("LD_ENABLE_SNAPSHOTS", False) in (
    True,
    "True",
    "true",
    "1",
)
LD_DISABLE_ASSET_UPLOAD = os.getenv("LD_DISABLE_ASSET_UPLOAD", False) in (
    True,
    "True",
    "true",
    "1",
)
LD_SINGLEFILE_PATH = os.getenv("LD_SINGLEFILE_PATH", "single-file")
LD_SINGLEFILE_UBLOCK_OPTIONS = os.getenv(
    "LD_SINGLEFILE_UBLOCK_OPTIONS",
    shlex.join(
        [
            '--browser-arg="--headless=new"',
            '--browser-arg="--user-data-dir=./chromium-profile"',
            '--browser-arg="--no-sandbox"',
            '--browser-arg="--load-extension=uBOLite.chromium.mv3"',
        ]
    ),
)
LD_SINGLEFILE_OPTIONS = os.getenv("LD_SINGLEFILE_OPTIONS", "")
LD_SINGLEFILE_TIMEOUT_SEC = float(os.getenv("LD_SINGLEFILE_TIMEOUT_SEC", 120))

# Monolith isn't used at the moment, as the local snapshot implementation
# switched to single-file after the prototype. Keeping this around in case
# it turns out to be useful in the future.
LD_MONOLITH_PATH = os.getenv("LD_MONOLITH_PATH", "monolith")
LD_MONOLITH_OPTIONS = os.getenv("LD_MONOLITH_OPTIONS", "-a -v -s")
