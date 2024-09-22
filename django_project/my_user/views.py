from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_view(request):
    title = "User Action"
    page_title = "User Action"

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if "register" in request.POST:
            # 確認用戶是否已經註冊
            if User.objects.filter(username=username).exists():
                msg = {
                    "code": 400,
                    "msg": "User already exists",
                }
            else:
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    is_staff=True,
                    is_superuser=True,
                )
                msg = {
                    "code": 200,
                    "msg": "User created successfully",
                }
        elif "login" in request.POST:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                msg = {
                    "code": 200,
                    "msg": "Login successfully",
                }
            else:
                msg = {
                    "code": 400,
                    "msg": "Login failed",
                }

        elif "logout" in request.POST:
            logout(request)
            msg = {
                "code": 200,
                "msg": "Logout successfully",
            }

    return render(request, "my_user.html", locals())
