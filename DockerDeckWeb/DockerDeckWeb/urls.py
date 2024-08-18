from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from .views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("add/<project>/", csrf_exempt(save_file)),
    path("<project>/<file_name>/", get_file, name="get_file"),
]
