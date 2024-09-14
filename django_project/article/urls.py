from django.urls import path
from .views import tag_view, tag_detail_view, create_or_update_article

urlpatterns = [
    path(
        "create_or_update_article/",
        create_or_update_article,
        name="create_or_update_article",
    ),
    path("tag/", tag_view, name="tag_view"),
    path("tag/<int:tag_id>/", tag_detail_view, name="tag_detail_view"),
]
