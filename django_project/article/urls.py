from django.urls import path
from .views import (
    tag_view,
    tag_detail_view,
    create_or_update_article,
    create_table_view,
    demo_form_view,
    article_list_view,
    article_detail_view,
    demo_model_form_view,
    # custom_admin_page,
    CustomAdminPageView,
)

urlpatterns = [
    path("demo_form/", demo_form_view, name="demo_form_view"),
    path("demo_model_form/", demo_model_form_view, name="demo_model_form_view"),
    path("article_list/", article_list_view, name="article_list_view"),
    path(
        "article_detail/<int:article_id>/",
        article_detail_view,
        name="article_detail_view",
    ),
    path(
        "create_or_update_article/",
        create_or_update_article,
        name="create_or_update_article",
    ),
    path("create_table/", create_table_view, name="create_table"),
    path("tag/", tag_view, name="tag_view"),
    path("tag/<int:tag_id>/", tag_detail_view, name="tag_detail_view"),
    # demo admin section
    # path("custom_admin_page/", custom_admin_page, name="custom_admin_page"),
    # path("custom_admin_page/", CustomAdminPageView.as_view(), name="custom_admin_page"),
]
