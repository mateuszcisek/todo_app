from typing import Any

from django.views.generic import RedirectView


class HomepageView(RedirectView):
    """Homepage view.

    It's purpose is to redirect the user to the list of the tasks.
    """

    permanent = True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        """Return the redirection URL.

        To make sure we return a correct URL, we use the reverse function to find the
        correct URL for the view with the list of the tasks.
        """
        from django.urls import reverse

        return reverse("todo:task-list")
