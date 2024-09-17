from django.contrib import admin

from .models import ArticleV2, Tag, Category, Author


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


class AuthorAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
    list_display = ["name", "age"]


admin.site.register(ArticleV2, ArticleAdmin)


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author, AuthorAdmin)
