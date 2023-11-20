from django.urls import include, re_path

from todo_app.core.views import HomepageView

urlpatterns = [
    re_path(r"^$", HomepageView.as_view(), name="homepage"),
    re_path(r"^todo/", include(("todo_app.todo.urls", "todo"))),
]
