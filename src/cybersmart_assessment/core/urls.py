from django.urls import include, re_path

from cybersmart_assessment.core.views import HomepageView

urlpatterns = [
    re_path(r"^$", HomepageView.as_view(), name="homepage"),
    re_path(r"^todo/", include(("cybersmart_assessment.todo.urls", "todo"))),
]
