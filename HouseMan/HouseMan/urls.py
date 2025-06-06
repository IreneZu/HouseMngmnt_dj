"""
URL configuration for HouseMan project.

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
from django.urls import path, include
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

from specifications.views import (platform, items_view, building_view
, building_spec, building_exp_view, building_exp_edit)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', platform),
    path('buildings/', building_view.as_view(), name='buildings'),
    path('sp_<int:building_id>/', building_spec, name='building_spec'),

    path('items', items_view.as_view()),

    path('view_<int:building_id>/', building_exp_view, name='building_exp_view'),
    path('edit_<int:building_id>/', building_exp_edit, name='building_exp_edit'),

]
