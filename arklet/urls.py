"""arklet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, re_path

from ark import views

minterpatterns = [
    path("mint", views.mint_ark, name="mint_ark"),
    path("update", views.update_ark, name="update_ark"),
    path("bulk_query", views.batch_query_arks, name="bulk_query"),
    path("bulk_update", views.batch_update_arks, name="bulk_update"),
    path("bulk_mint", views.batch_mint_arks, name="bulk_mint"),
    path("admin/", admin.site.urls),
]

resolverpatterns = [
    re_path(r"^(resolve/)?(?P<ark>ark:/?.*$)", views.resolve_ark, name="resolve_ark"),
    path("", views.status, name="status"),
]

combinedpatterns = minterpatterns + resolverpatterns

urlpatterns = resolverpatterns if os.environ.get("RESOLVER") else combinedpatterns

