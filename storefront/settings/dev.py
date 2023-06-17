from .common import *

DEBUG = True
SECRET_KEY = "django-insecure-msm19@m$$6rv%_#s_a%z4jmu1apwb%vdauim8kn()@fim#f1p!"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
