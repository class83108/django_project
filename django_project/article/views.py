from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
from django.contrib.admin.sites import site

from .models import Tag, Article, create_table, Category, Author, ArticleV2
from .forms import ArticleForm, ArticleModelForm
from utility import get_tags_count

import json

import time


def article_view(request):
    articles = Article.objects.all()  # 取得所有文章
    article = Article.objects.get(article_id=1)  # 取得文章 id=1 的文章
    article, created = Article.objects.get_or_create(
        title="Hello", content="World"
    )  # 取得或新增文章
    articles = Article.objects.filter(title__contains="Hello")  # 篩選文章
    articles = Article.objects.exclude(title__contains="Hello")  # 排除文章
    articles = Article.objects.order_by("-created_at")  # 排序文章
    articles = Article.objects.order_by("created_at")[0:2]  # 取得前兩篇文章
    return render(request, "article.html", {"articles": articles})


def article_list_view(request):
    articles = ArticleV2.objects.all()
    return render(request, "article_list.html", {"articles": articles})


def article_detail_view(request, article_id):
    article = get_object_or_404(ArticleV2, article_id=article_id)
    article_form = ArticleModelForm(instance=article)
    return render(request, "article_detail.html", {"article_form": article_form})


def search_articles(request):
    article_query = request.GET.get("article_query")
    articles = Article.objects.filter(
        Q(title__contains=article_query) | Q(content__contains=article_query)
    )


def create_or_update_article(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        try:
            article = get_object_or_404(Article, title=title)
            article.content = request.POST["content"]
            article.save()
        except:
            article = Article.objects.create(title=title, content=content)
    return render(request, "article_detail.html", locals())


# 聚合
def article_aggregate_view(request):
    articles = Article.objects.annotate(
        category_count=Count("category"),  # 計算文章的分類數量
    )


def tag_view(request):
    tags = Tag.objects.all()
    return render(request, "tag.html", {"tags": tags})


def tag_detail_view(request, tag_id):
    tag = Tag.objects.get(tag_id=tag_id)
    return render(request, "tag_detail.html", {"tag": tag})


def create_table_view(request):
    today = time.localtime(time.time())
    article = Article.objects.get(article_id=2)
    model_name = f"{article.article_id}_{time.strftime('%Y%m%d', today)}_view"

    new_model = create_table(model_name=model_name)
    new_model.objects.create(
        views=0,
        date=today,
        article=article,
    )
    return JsonResponse({"status": "success"})


def demo_form_view(request):
    article_form = ArticleForm()
    error = None
    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data["title"]
            content = article_form.cleaned_data["content"]
            category = article_form.cleaned_data["category"]
            author = article_form.cleaned_data["author"]
            tags = article_form.cleaned_data["tags"]

            article = Article.objects.create(
                title=title, content=content, category=category, author=author
            )
            article.tags.set(tags)
            return redirect("article:article_list_view")
        else:
            error = article_form.errors

    return render(request, "demo_form.html", locals())


def demo_model_form_view(request):
    article_form = ArticleModelForm()
    error = None
    if request.method == "POST":
        article_form = ArticleModelForm(request.POST, request.FILES)
        if article_form.is_valid():
            print(article_form.cleaned_data)
            article_form.save()
            return redirect("article:article_list_view")
        else:
            error = article_form.errors

    return render(request, "demo_form.html", locals())


# def custom_admin_page(request):
#     return render(request, "custom_admin_page.html", locals())


# class CustomAdminPageView(TemplateView):
#     template_name = "custom_admin_page.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context.update(site.each_context(self.request))
#         print(context)
#         return context

from django.contrib.admin.views.main import ERROR_FLAG


class CustomAdminPageView(TemplateView):
    template_name = "admin/custom_admin_page.html"
    admin_site = None  # 初始化 admin_site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 獲取原始的上下文數據

        # 獲取傳遞的 AdminSite 實例
        admin_site = self.admin_site or self.request.site

        if admin_site:
            # 獲取完整的 admin 上下文
            admin_context = admin_site.each_context(self.request)
            context.update(admin_context)

            # 添加額外的上下文數據
            context.update(
                {
                    "title": "Custom Admin Page",
                    "subtitle": None,
                    # 是否為 popup
                    "is_popup": False,
                    "has_permission": self.request.user.is_active
                    and self.request.user.is_staff,
                    # 是否啟用側邊欄
                    "is_nav_sidebar_enabled": admin_context.get(
                        "is_nav_sidebar_enabled", True
                    ),
                    # 獲取應用列表
                    "available_apps": admin_site.get_app_list(self.request),
                    ERROR_FLAG: admin_context.get(ERROR_FLAG, ""),
                    "tag_count_result": json.loads(get_tags_count()),
                }
            )

        return context

    # 重寫as_view方法，保存添加admin_site屬性
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.admin_site = initkwargs.get("admin_site")
        return view
