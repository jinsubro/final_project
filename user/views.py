from http.client import HTTPResponse
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from user.models import User


from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    if request.method == "POST":
        print(f"[test] POST")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            #user = authenticate(username=username,password=raw_password) # 대체 필요
            user = User.objects.get(username=username)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HTTPResponse('로그인 실패. 다시 시도해주세요.')
            # try:
            #     user = User.objects.get()
            # except User.DoesNotExist:
            #     pass
            # else:
            #     if user.check_password(raw_password):
            #         msg = None
            #         login(request, user)
            #         is_ok = True
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요						
    else:
        print(f"else")
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요						
    logout(request)
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    cur_user = request.user
    if cur_user.is_authenticated:
        page = int(request.GET.get("page", 1))
        users = User.objects.all().order_by("-id")
        paginator = Paginator(users, 10)
        users = paginator.get_page(page)
        return render(request, "users.html", {"users": users})
    else:
        return HttpResponseRedirect("/login")