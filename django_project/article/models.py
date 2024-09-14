from django.db import models


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=120, verbose_name="Title", unique=True, null=False
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    age = models.IntegerField()


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)


class DemoManager(models.Manager):
    def is_active(self):
        return self.filter(is_active=True)


class DemoModel(models.Model):
    name = models.CharField(max_length=120)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")
    objects = DemoManager()

    class Meta:
        db_table = "demo_model"  # 設置資料表名稱
        verbose_name = "Demo Model"  # 設置在admin後台顯示的名稱
        verbose_name_plural = "Demo Model"  # 設置在admin後台顯示的名稱（複數形式）
        ordering = ["-created_at"]  # 設置資料排序方式 - 表示降序，默認表示升序
        abstract = True  # 設置為抽象模型，不會生成資料表
        unique_together = ["name", "age"]  # 設置唯一索引
        indexes = [models.Index(fields=["name", "age"])]  # 設置索引
        permissions = [("can_read_demo_model", "Can read demo model")]  # 設置權限
        app_label = "article"  # 設置應用名稱 如果不設置則默認為應用名稱

    def __str__(self):
        return self.name  # 返回模型實例的名稱

    def save(self, *args, **kwargs):
        # 可以自定義保存邏輯
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 可以自定義刪除邏輯
        super().delete(*args, **kwargs)

    def clean(self) -> None:
        # 可以自定義驗證邏輯 例如驗證name是否為空 通常用於表單驗證
        if not self.name:
            raise ValueError("name cannot be empty")
        return super().clean()

    def get_absolute_url(self):
        # 返回模型實例的絕對URL
        return f"/demo_model/{self.pk}/"


class DemoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
