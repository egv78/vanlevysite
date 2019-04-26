"""vanlevysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vanlevy.urls', namespace='vanlevy')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('swdice/', include('swdice.urls', namespace='swdice')),
    path('gendice/', include('gendice.urls', namespace='gendice')),
    path('polydice/', include('polydice.urls', namespace='polydice')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

