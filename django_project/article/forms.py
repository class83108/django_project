from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import transaction
from django.core.files.uploadedfile import UploadedFile


from .models import Category, Author, Tag, Article, ArticleV2

import json
import re
import os


class JSONBMarkdownField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.Textarea(attrs={"name": "content"})
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if value is None:
            return ""
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return value
        return self.jsonb_to_markdown(value)

    def clean(self, value):
        value = super().clean(value)
        return self.markdown_to_jsonb(value)

    def jsonb_to_markdown(self, jsonb_data):
        markdown = ""
        for item in jsonb_data.get("content", []):
            if item["type"] == "paragraph":
                texts = item["text"].split("\n")
                for text in texts:
                    markdown += text + "\n"
            elif item["type"] in ["h1", "h2", "h3"]:
                markdown += f"{'#' * int(item['type'][1])} {item['text']}\n"
            elif item["type"] == "list":
                markdown += self.process_list(item)
            elif item["type"] == "image":
                markdown += f"![{item.get('alt', '')}]({item['src']})"
                if "width" in item:
                    markdown += f"{{width-{item['width']}}}"
                markdown += "\n"
            elif item["type"] == "table":
                markdown += self.process_table(item)
            elif item["type"] == "link":
                markdown += f"[{item['text']}]({item['url']})"
            elif item["type"] == "empty_line":
                markdown += "\n"
            elif item["type"] == "blockquote":
                markdown += f"> {item['text']}\n"

        return markdown.strip()

    def process_list(self, list_item):
        markdown = ""
        for index, item in enumerate(list_item["items"], start=1):
            prefix = "-" if list_item.get("style") == "unordered" else f"{index}."
            markdown += f"{prefix} {item['text']}\n"
            if item.get("description"):
                markdown += f"   {item['description']}\n"
        return markdown + "\n"

    def process_table(self, table):
        markdown = "| " + " | ".join(table["headers"]) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(table["headers"])) + " |\n"
        for row in table["rows"]:
            markdown += (
                "| "
                + " | ".join(str(row.get(header, "")) for header in table["headers"])
                + " |\n"
            )
        return markdown + "\n"

    def markdown_to_jsonb(self, markdown):
        lines = markdown.split("\n")
        jsonb_content = []
        current_list = None
        current_table = None

        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                level = len(line.split()[0])
                jsonb_content.append(
                    {"type": f"h{level}", "text": line.lstrip("#").strip()}
                )
                current_list = None
                current_table = None
            elif (
                line.startswith("- ")
                or re.match(r"^\d+\.", line)
                or line.startswith("* ")
            ):
                if current_list is None or (current_list["style"] == "ordered") != bool(
                    re.match(r"^\d+\.", line)
                ):
                    if current_list:
                        jsonb_content.append(current_list)
                    current_list = {
                        "type": "list",
                        "style": "unordered" if line.startswith("- ") else "ordered",
                        "items": [],
                    }
                text = re.sub(r"^-|\d+\.\s*", "", line).strip()
                current_list["items"].append({"text": text})
            elif line.startswith("!["):
                match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)(\{width-(\d+)\})?", line)
                if match:
                    image = {
                        "type": "image",
                        "alt": match.group(1),
                        "src": match.group(2),
                    }
                    if match.group(4):
                        image["width"] = int(match.group(4))
                    jsonb_content.append(image)
                current_list = None
                current_table = None
            elif line.startswith("|"):
                if current_table is None:
                    current_table = {"type": "table", "headers": [], "rows": []}
                    jsonb_content.append(current_table)
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                if not current_table["headers"]:
                    current_table["headers"] = cells
                elif all(cell == "---" for cell in cells):
                    continue
                else:
                    row = {
                        header: cell
                        for header, cell in zip(current_table["headers"], cells)
                    }
                    current_table["rows"].append(row)
                current_list = None
            elif re.match(r"\[.*\]\(.*\)", line):
                match = re.match(r"\[(.*?)\]\((.*?)\)", line)
                link = {"type": "link", "text": match.group(1), "url": match.group(2)}
                jsonb_content.append(link)
                current_list = None
                current_table = None
            # 處理空行
            elif (
                not line
                and jsonb_content
                and jsonb_content[-1].get("type") != "empty_line"
            ):
                jsonb_content.append({"type": "empty_line"})
                current_list = None
                current_table = None
            elif line.startswith(">"):
                jsonb_content.append({"type": "blockquote", "text": line[1:].strip()})
                current_list = None
                current_table = None
            elif line:
                jsonb_content.append({"type": "paragraph", "text": line})
                current_list = None
                current_table = None
            else:
                if current_list:
                    jsonb_content.append(current_list)
                    current_list = None
                current_table = None

        if current_list:
            jsonb_content.append(current_list)

        return {"content": jsonb_content}


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=120)
    content = JSONBMarkdownField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())


def validate_file_size(value):
    filesize = value.size
    if filesize > 1 * 1024 * 1024:
        raise ValidationError("檔案大小不能超過1MB。")


class ArticleModelForm(forms.ModelForm):

    cover = forms.ImageField(
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_file_size,
        ],
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    class Meta:
        model = ArticleV2
        fields = [
            "title",
            "content",
            "category",
            "author",
            "tags",
            "cover",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"] = JSONBMarkdownField()
        self.fields["content"].label = "Content"
        self.fields["content"].initial = self.instance.content
        self.fields["content"].required = False

        self.fields["tags"].queryset = Tag.objects.all()
        self.fields["category"].queryset = Category.objects.all()
        self.fields["author"].queryset = Author.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        article = super().save(commit=False)

        if commit:
            with transaction.atomic():
                article.save()
                self.save_m2m()

                # 獲取上傳的文件
                cover = self.cleaned_data.get("cover")
                if cover and isinstance(cover, UploadedFile):
                    # 獲取原始文件的擴展名
                    _, file_extension = os.path.splitext(cover.name)

                    # 創建新的文件名，使用 article_id
                    new_file_name = f"article_{article.article_id}{file_extension}"

                    # 設置新的文件名
                    article.cover.save(new_file_name, cover, save=True)

        return article
