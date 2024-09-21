from django.db import models
from typing import Dict, Any, Optional, Type, Callable
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import JSONField
from django import forms

import json
import re


from mdeditor.fields import MDTextField


def create_model(
    name: str,
    fields: Optional[Dict[str, Any]] = None,
    app_label: str = "",
    options: Optional[Dict[str, Any]] = None,
) -> Type[models.Model]:
    """
    創建模型
    :param name: 模型名稱
    :param fields: 模型欄位
    :param app_label: 應用名稱
    :param options: 模型選項
    :return: 模型類
    """

    class Meta:
        pass

    setattr(Meta, "app_label", app_label)

    # 設置模型的meta選項
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)

    # 設置模型的欄位
    attrs: Dict[str, Any] = {"__module__": f"{app_label}.models", "Meta": Meta}
    if fields:
        attrs.update(fields)

    # 創建模型
    model: Type[models.Model] = type(name, (models.Model,), attrs)
    return model


def create_db(model: Type[models.Model]) -> None:
    """
    創建資料表
    :param model: 模型類
    """
    from django.db import connection
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor

    try:
        with BaseDatabaseSchemaEditor(connection) as schema_editor:
            schema_editor.create_model(model=model)
    except Exception as e:
        pass


def create_table(model_name: str) -> Type[models.Model]:
    """
    創建資料表
    :param model_name: 模型名稱
    :return: 模型類
    """
    fields: Dict[str, Any] = {
        "id": models.AutoField(primary_key=True),
        "views": models.IntegerField(default=0),
        "date": models.DateField(auto_now_add=True),
        "article": models.ForeignKey("Article", on_delete=models.CASCADE),
        "__str__": lambda self: f"{self.article.title}_{self.date}_views",
    }

    options: Dict[str, str] = {
        "verbose_name": model_name,
        "verbose_name_plural": model_name,
    }

    model: Type[models.Model] = create_model(
        name=model_name, fields=fields, app_label="article", options=options
    )
    create_db(model)
    return model


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=120, verbose_name="Title", unique=True, null=False
    )
    # content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")

    # 新增欄位
    cover_name = models.CharField(max_length=120, null=True)
    # 修改欄位
    content = JSONField(default=dict)

    class Meta:
        app_label = "article"


class ArticleV2(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=120,
        unique=True,
        null=False,
        verbose_name="標題",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="分類"
    )
    author = models.ForeignKey("Author", on_delete=models.CASCADE, verbose_name="作者")
    tags = models.ManyToManyField("Tag", verbose_name="標籤")

    # 新增欄位
    cover = models.ImageField(
        upload_to="static/images/cover_image", null=True, verbose_name="封面"
    )
    # 修改欄位
    content = JSONField(default=dict, verbose_name="內容")
    # content = MDTextField(verbose_name="內容")

    def __str__(self) -> str:
        return self.title

    class Meta:
        app_label = "article"
        verbose_name = "文章"
        verbose_name_plural = "文章"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "article"
        verbose_name = "分類"
        verbose_name_plural = "分類"


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "article"
        verbose_name = "作者"
        verbose_name_plural = "作者"


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "article"
        verbose_name = "標籤"
        verbose_name_plural = "標籤"


# class DemoManager(models.Manager):
#     def is_active(self):
#         return self.filter(is_active=True)


# class DemoModel(models.Model):
#     name = models.CharField(max_length=120)
#     age = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#     category = models.ForeignKey("Category", on_delete=models.CASCADE)
#     author = models.ForeignKey("Author", on_delete=models.CASCADE)
#     tags = models.ManyToManyField("Tag")
#     objects = DemoManager()

#     class Meta:
#         db_table = "demo_model"  # 設置資料表名稱
#         verbose_name = "Demo Model"  # 設置在admin後台顯示的名稱
#         verbose_name_plural = "Demo Model"  # 設置在admin後台顯示的名稱（複數形式）
#         ordering = ["-created_at"]  # 設置資料排序方式 - 表示降序，默認表示升序
#         abstract = True  # 設置為抽象模型，不會生成資料表
#         unique_together = ["name", "age"]  # 設置唯一索引
#         indexes = [models.Index(fields=["name", "age"])]  # 設置索引
#         permissions = [("can_read_demo_model", "Can read demo model")]  # 設置權限
#         app_label = "article"  # 設置應用名稱 如果不設置則默認為應用名稱

#     def __str__(self):
#         return self.name  # 返回模型實例的名稱

#     def save(self, *args, **kwargs):
#         # 可以自定義保存邏輯
#         super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         # 可以自定義刪除邏輯
#         super().delete(*args, **kwargs)

#     def clean(self) -> None:
#         # 可以自定義驗證邏輯 例如驗證name是否為空 通常用於表單驗證
#         if not self.name:
#             raise ValueError("name cannot be empty")
#         return super().clean()

#     def get_absolute_url(self):
#         # 返回模型實例的絕對URL
#         return f"/demo_model/{self.pk}/"


# class DemoManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_active=True)
