from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route

"""
ViewSet classes are almost the same thing as View classes, except that they
provide operations such as read, or update, and not method handlers such as
get or put.

A ViewSet class is only bound to a set of method handlers at the last moment,
when it is instantiated into a set of views, typically by using a Router
class which handles the complexities of defining the URL conf for you.
"""


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""
Here we've used the ReadOnlyModelViewSet class to automatically provide the
default 'read-only' operations. We're still setting the queryset and
serializer_class attributes exactly as we did when we were using regular
views, but we no longer need to provide the same information to two
separate classes.
"""


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

"""
This time we've used the ModelViewSet class in order to get the complete set
of default read and write operations.

Notice that we've also used the @detail_route decorator to create a custom
action, named highlight. This decorator can be used to add any custom
endpoints that don't fit into the standard create/update/delete style.

Custom actions which use the @detail_route decorator will respond to GET
requests. We can use the methods argument if we wanted an action that
responded to POST requests.

The URLs for custom actions by default depend on the method name itself. If
you want to change the way url should be constructed, you can include
url_path as a decorator keyword argument.
"""
