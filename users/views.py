from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect


class LoginView(BaseLoginView):
    template_name = "users/login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
