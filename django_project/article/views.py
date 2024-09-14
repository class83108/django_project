from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count


from .models import Tag, Article, Category, Author


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
