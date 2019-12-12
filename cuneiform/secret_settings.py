
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SUPER_SECRET_KEY = 'eurm6@ov0v%k*02@lz+$b!bhn79sy1lz_77%6)eg(-zt#xs2=^'

SUPER_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'cuneiform.sqlite3'),
        'TEST': { 
		'NAME':  'test_cuneiform.sqlite3'),
	}
    }
}



SUPER_USE_TZ = True


