from django.shortcuts import render
from django.urls import reverse


def index_view(request, user_name, age, page_name, user_id):

    url_info = {
        "user_name": user_name,
        "user_name_type": type(user_name).__name__,
        "age": age,
        "age_type": type(age).__name__,
        "page_name": page_name,
        "page_name_type": type(page_name).__name__,
        "user_id": user_id,
        "user_id_type": type(user_id).__name__,
    }
    print(url_info)
    return render(request, "index.html", {"url_info": url_info})


def demo_path_view(request, to_inde_page):

    return render(
        request,
        "index.html",
        {
            "to_inde_page": to_inde_page,
            "to_inde_page_type": type(to_inde_page).__name__,
        },
    )


def demo_view(request):
    url = reverse("article:tag_detail_view", args=[1])

    return render(request, "demo.html", {"url": url})


def demo_html_tag_view(request):
    samoyed_content = "The Samoyed is a breed of large herding dog that descended from the Nenets herding laika, a spitz-type dog, with a thick, white, double-layer coat."

    golden_retriever_content = "The Golden Retriever is a medium-large gun dog that was bred to retrieve shot waterfowl, such as ducks and upland game birds, during hunting and shooting parties."

    return render(
        request,
        "demo_html_tag.html",
        {
            "samoyed_content": samoyed_content,
            "golden_retriever_content": golden_retriever_content,
        },
    )
