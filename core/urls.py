from django.contrib import admin
from django.urls import path, include
from django.urls import re_path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('', include('bot.urls')),
    path('', include('swagger.urls'))
]
