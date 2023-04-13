"""
URL configuration for paymob project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from django.db import connection
from app.views.table_view import DynamicModelView, DataViewset


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "create_dynamic_model/",
        DynamicModelView.as_view({"post": "create"}),
        name="create_dynamic_model",
    ),
    path(
        "create_dynamic_model/<int:pk>",
        DynamicModelView.as_view({"put": "update"}),
        name="create_dynamic_model",
    ),
    path("data/<int:pk>/rows", DataViewset.as_view({"get": "list"}), name="data_model"),
    path(
        "data/<int:pk>/row", DataViewset.as_view({"post": "create"}), name="data_model"
    ),
]
