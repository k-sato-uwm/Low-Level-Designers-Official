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
from django.contrib import admin
from django.urls import path
from scheduler.views import  UserManagementView, LoginView, Dashboard, CourseManagement,CourseEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usermanagement/', UserManagementView.as_view(), name='UserManagement'),
    path('dashboard/', Dashboard.as_view()),
    #path('login', Create.as_view(), name='login'),
    path('', LoginView.as_view(), name='login'),
    path('courses/', CourseManagement.as_view(), name='course_management'),
    path('courses/<int:course_id>/', CourseEditView.as_view(), name='edit_course'),

]
