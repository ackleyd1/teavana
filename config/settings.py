import os
import braintree

from unipath import Path
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)

ROOT_DIR = Path(__file__).ancestor(2)


SECRET_KEY = get_env_variable('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['ravedave.co', 'web']
WSGI_APPLICATION = 'config.wsgi.application'
ROOT_URLCONF = 'core.urls'

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Application definition

LOCAL_APPS = [
    'carts',
    'core',
    'teas',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

INSTALLED_APPS = LOCAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS

# Middleware definition

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates definition

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT_DIR.child('templates')],
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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Database definition

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Password validators definition

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


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR.child('static')

MEDIA_URL = '/media/'
MEDIA_ROOT = ROOT_DIR.child('media')

# Allauth

LOGIN_REDIRECT_URL = "/"

SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {'login': 'core.forms.CrispyLoginForm', 'signup': 'core.forms.CrispySignupForm'}


DEFAULT_FROM_EMAIL = "ackleyd1@msu.edu"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.sendgrid.com"
EMAIL_HOST_USER = "ackleyd1"
EMAIL_MAIN = "ackleyd1@msu.edu"
EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USER_TLS = False

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

BRAINTREE_MERCHANT_ID = get_env_variable("BRAINTREE_MERCHANT_ID")
BRAINTREE_PUBLIC_KEY = get_env_variable("BRAINTREE_PUBLIC_KEY")
BRAINTREE_PRIVATE_KEY = get_env_variable("BRAINTREE_PRIVATE_KEY")

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id=BRAINTREE_MERCHANT_ID,
    public_key=BRAINTREE_PUBLIC_KEY,
    private_key=BRAINTREE_PRIVATE_KEY
)
