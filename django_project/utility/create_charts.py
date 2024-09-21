from article.models import Tag
from django.db.models import Count

import json


def get_tags_count() -> dict:
    tags_count = Tag.objects.annotate(count=Count("articlev2")).values_list(
        "name", "count"
    )

    return json.dumps(
        {
            "labels": [tag[0] for tag in tags_count],
            "data": [tag[1] for tag in tags_count],
        }
    )
