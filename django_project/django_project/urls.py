"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from article.admin import admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from .views import index_view, demo_path_view, demo_view, demo_html_tag_view


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin_site.urls),
    path("article/", include(("article.urls", "article"), namespace="article")),
    path("chat/", include(("chat.urls", "chat"), namespace="chat")),
    # path("<str:user_name>/<int:age>/<slug:page_name>/<uuid:user_id>", index_view),
    # path("<path:to_inde_page>", demo_path_view),
    path("demo/", demo_view),
    path("demo_html_tag/", demo_html_tag_view),
)


# urlpatterns = [
#     # path("admin/", admin.site.urls),
#     path("admin/", admin_site.urls),
#     path("article/", include(("article.urls", "article"), namespace="article")),
#     path("chat/", include(("chat.urls", "chat"), namespace="chat")),
#     # path("<str:user_name>/<int:age>/<slug:page_name>/<uuid:user_id>", index_view),
#     # path("<path:to_inde_page>", demo_path_view),
#     path("demo/", demo_view),
#     path("demo_html_tag/", demo_html_tag_view),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
