"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


# for swagger
schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Alex Team's BlankHouse Project APIS",
        default_version="1.0.0",
        description="API documentation. Below are all of the possible response codes with a short description.",
    ),
    public=True,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users", include("users.urls")),
    path("api/v1/categories", include("categories.urls")),
    path("api/v1/rooms", include("rooms.urls")),
    path("api/v1/experiences", include("experiences.urls")),
    path("api/v1/photos", include("photos.urls")),
    path(
        "api/v1/swagger/schema/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-schema",
    ),
]
