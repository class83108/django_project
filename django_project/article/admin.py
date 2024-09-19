from typing import Any
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.forms import ModelForm
from django.http import HttpRequest
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from article.views import CustomAdminPageView as CustomView

import re


from .models import ArticleV2, Tag, Category, Author


class CustomAdminPageView(admin.AdminSite):
    # 自定義 admin 頁面 除了原本的 urls 之外,再添加一個自定義的 url
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "custom_admin_page/",
                self.admin_view(CustomView.as_view(admin_site=self)),
                name="custom_admin_page",
            ),
        ]
        return custom_urls + urls

    # 自定義 admin 頁面的左側導航欄
    def get_app_list(self, request: WSGIRequest) -> list[Any]:
        app_list = super().get_app_list(request)

        custom_admin_url = reverse("admin:custom_admin_page")

        app_list.append(
            {
                "name": _("Custom Admin Page"),
                "app_label": "custom_admin_page",
                "app_url": "",
                "has_module_perms": True,
                "models": [
                    {
                        "name": _("Custom Admin Page"),
                        "object_name": "CustomAdminPage",
                        "admin_url": custom_admin_url,
                    }
                ],
            }
        )
        return app_list


class ArticleInline(admin.TabularInline):
    model = ArticleV2
    extra = 1


class ArticleAdmin(admin.ModelAdmin):

    # 在列表頁顯示的欄位
    list_display = ["title", "created_at", "updated_at"]

    # 在列表頁可以搜尋的欄位
    search_fields = ["title"]

    # 在列表頁可以篩選的欄位
    list_filter = ["created_at", "updated_at"]

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = "Tags"
    # 添加自定義的欄位
    list_display += ["get_tags"]

    def get_readonly_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> list[str] | tuple[Any, ...]:
        if request.user.is_superuser:
            self.readonly_fields = []
        else:
            self.readonly_fields = ["cover"]
        return self.readonly_fields

    def get_queryset(self, request: HttpRequest) -> Any:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(article_id__lt=2)

    def save_model(
        self, request: HttpRequest, obj: Any, form: ModelForm, change: bool
    ) -> None:
        if change:
            article_title = form.cleaned_data["title"]
            pattern = r"(.*)\.v(\d+)$"
            match = re.match(pattern, article_title)

            if match:
                base_title = match.group(1)
                version = int(match.group(2))
                new_version = version + 1
                new_title = f"{base_title}.v{new_version}"
            else:
                new_title = f"{article_title}.v1"
        else:
            # 如果是新建文章,添加 .v1
            new_title = f"{form.cleaned_data['title']}.v1"

        # 更新文章標題
        obj.title = new_title
        super().save_model(request, obj, form, change)

    def add_version(self, request: HttpRequest, queryset: Any) -> None:
        for article in queryset:
            article_title = article.title
            pattern = r"(.*)\.v(\d+)$"
            match = re.match(pattern, article_title)

            if not match:
                new_title = f"{article_title}.v1"
                article.title = new_title
                article.save()
        self.message_user(request, "Add version successfully")

    add_version.short_description = "Add version"
    actions = ["add_version"]

    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",
            )
        }

        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js",
            "js/init_select2.js",
        )


class AuthorAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
    list_display = ["name", "age"]


admin_site = CustomAdminPageView(name="admin")

admin_site.register(ArticleV2, ArticleAdmin)
admin_site.register(Tag)
admin_site.register(Category)
admin_site.register(Author, AuthorAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)

# admin.site.register(ArticleV2, ArticleAdmin)


# admin.site.register(Tag)
# admin.site.register(Category)
# admin.site.register(Author, AuthorAdmin)
