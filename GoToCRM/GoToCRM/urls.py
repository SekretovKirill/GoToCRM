"""GoToCRM URL Configuration

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
from crm.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('student', details),
    path('add', add),
    path('edit', edit),
    path('delete', delete),
    path('courses', courslist),
    path('course', coursedet),
    path('editcourse', editcourse),
    path('courslist', courslist),
    path('coursedet', coursedet),
    path('addcourse', addcourse),
    path('delcourse', delcourse),
    path('register', register),
    path('login', login_page),
    path('logout', logout_page),

]
