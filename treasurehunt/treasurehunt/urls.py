from django.contrib import admin
from django.urls import path
from treasurehunt.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
  path('admin/', admin.site.urls),
  path('about/', about),
  path('info/', info),
  path('', home),
]

urlpatterns += staticfiles_urlpatterns()