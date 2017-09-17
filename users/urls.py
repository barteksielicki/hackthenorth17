from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from users.views import LoginView

urlpatterns = [
    url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^logout/$", LogoutView.as_view(next_page="/"), name="logout")
]