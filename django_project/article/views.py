from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.http import JsonResponse

from .models import Tag, Article, create_table, Category, Author, ArticleV2
from .forms import ArticleForm, ArticleModelForm

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
