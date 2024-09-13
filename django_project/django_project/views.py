from django.shortcuts import render


def index_view(request, user_name, age, page_name):

    url_info = {
        "user_name": user_name,
        "user_name_type": type(user_name),
        "age": age,
        "age_type": type(age),
        "page_name": page_name,
        "page_name_type": type(page_name),
    }

    return render(request, "index.html", url_info)
