from django.urls import path
from .views import (
    tag_view,
    tag_detail_view,
    create_or_update_article,
    create_table_view,
)

urlpatterns = [
    path(
        "create_or_update_article/",
        create_or_update_article,
        name="create_or_update_article",
    ),
    path("create_table/", create_table_view, name="create_table"),
    path("tag/", tag_view, name="tag_view"),
    path("tag/<int:tag_id>/", tag_detail_view, name="tag_detail_view"),
]
