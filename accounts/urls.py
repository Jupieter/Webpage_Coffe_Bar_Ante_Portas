from django.urls import path, include
from .views import login_page, register_page, token_gen
from django.contrib.auth.views import LogoutView, LoginView

app_name = "accounts"

urlpatterns = [
    # path('login/', LoginView.as_view(), name="login"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('token_gen/', token_gen, name="token_gen"),
]

# urlpatterns = [path('accounts/', include('django.contrib.auth.urls'))]