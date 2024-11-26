"""
URL configuration for TA_Scheduler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from scheduler.views import Create

from django.contrib import admin
from django.urls import path
from scheduler.views import Create

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('scheduler/', Create.as_view(), name='Create'),  # Scheduler view
    path('', Create.as_view(), name='home'),  # Root URL as the homepage
]