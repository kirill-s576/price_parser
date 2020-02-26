"""project_two URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^sells/', include('sells.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^goose_card/', include('goose_card.urls')),
    url(r'^ironparsermain/', include('iron_parser.urls')),
    url(r'^ironparserresults/', include('results.urls')),
    url(r'^authorisation/', include('authorisation.urls')),
    url(r'^', include('main.urls')),


]
