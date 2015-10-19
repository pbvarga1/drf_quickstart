from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer


# """
# Let's see how we can write some API views using our new Serializer class.
# For the moment we won't use any of REST framework's other features, we'll just
# write the views as regular Django views.

# We'll start off by creating a subclass of HttpResponse that we can use to
# render any data we return into json.
# """


# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

#     """
#     The root of our API is going to be a view that supports listing all the
#     existing snippets, or creating a new snippet.
#     """

#     @csrf_exempt
#     def snippet_list(request):
#         """
#         List all code snippets, or create a new snippet.
#         """
#         if request.method == 'GET':
#             snippets = Snippet.objects.all()
#             serializer = SnippetSerializer(snippets, many=True)
#             return JSONResponse(serializer.data)

#         elif request.method == 'POST':
#             data = JSONParser().parse(request)
#             serializer = SnippetSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JSONResponse(serializer.data, status=201)
#             return JSONResponse(serializer.errors, status=400)

#     """Note that because we want to be able to POST to this view from clients
#     that won't have a CSRF token we need to mark the view as csrf_exempt.
#     This isn't something that you'd normally want to do, and REST framework
#     views actually use more sensible behavior than this, but it'll do for
#     our purposes right now.

#     We'll also need a view which corresponds to an individual snippet, and
#     can be used to retrieve, update or delete the snippet.
#     """

#     @csrf_exempt
#     def snippet_detail(request, pk):
#         """
#         Retrieve, update or delete a code snippet.
#         """
#         try:
#             snippet = Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return HttpResponse(status=404)

#         if request.method == 'GET':
#             serializer = SnippetSerializer(snippet)
#             return JSONResponse(serializer.data)

#         elif request.method == 'PUT':
#             data = JSONParser().parse(request)
#             serializer = SnippetSerializer(snippet, data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JSONResponse(serializer.data)
#             return JSONResponse(serializer.errors, status=400)

#         elif request.method == 'DELETE':
#             snippet.delete()
#             return HttpResponse(status=204)

# """
# Our instance view is an improvement over the previous example. It's a
# little more concise, and the code now feels very similar to if we were
# working with the Forms API. We're also using named status codes, which makes
# the response meanings more obvious.

# To take advantage of the fact that our responses are no longer hardwired to
# a single content type let's add support for format suffixes to our API
# endpoints. Using format suffixes gives us URLs that explicitly refer to a
# given format, and means our API will be able to handle URLs such
# as http://example.com/api/items/4/.json.
# """


# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     """
#     List all snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


"""
We can also write our API views using class based views, rather than function
based views. As we'll see this is a powerful pattern that allows us to reuse
common functionality, and helps us keep our code DRY.
"""

# from rest_framework import mixins
# from rest_framework import generics


# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     It looks pretty similar to the previous case, but we've got better
#     separation between the different HTTP methods.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
One of the big wins of using class based views is that it allows us to easily
compose reusable bits of behaviour.

The create/retrieve/update/delete operations that we've been using so far are
going to be pretty similar for any model-backed API views we create. Those
bits of common behaviour are implemented in REST framework's mixin classes.

We'll take a moment to examine exactly what's happening here. We're building
our view using GenericAPIView, and adding in ListModelMixin and
CreateModelMixin.

The base class provides the core functionality, and the mixin classes provide
the .list() and .create() actions. We're then explicitly binding the get and
post methods to the appropriate actions. Simple enough stuff so far.
"""


# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

"""
Pretty similar. Again we're using the GenericAPIView class to provide the
core functionality, and adding in mixins to provide the .retrieve(),
.update() and .destroy() actions.
"""

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

"""
Using the mixin classes we've rewritten the views to use slightly less code
than before, but we can go one step further. REST framework provides a set
of already mixed-in generic views that we can use to trim down our views.py
module even more.

REST framework includes a number of permission classes that we can use to
restrict who can access a given view. In this case the one we're looking for
is IsAuthenticatedOrReadOnly, which will ensure that authenticated requests
get read-write access, and unauthenticated requests get read-only access.
"""

from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly


# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def perform_create(self, serializer):
#         """Allows us to modify how the instance save is managed, and handle
#         any information that is implicit in the incoming request or requested
#         URL.
#         """
#         serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)


from django.contrib.auth.models import User


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

"""
Create Entry point to API

Two things should be noticed here. First, we're using REST framework's reverse
function in order to return fully-qualified URLs; second, URL patterns are
identified by convenience names that we will declare later on in our
snippets/urls.py.
"""


# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })


"""
The other obvious thing that's still missing from our pastebin API is the
code highlighting endpoints.

Unlike all our other API endpoints, we don't want to use JSON, but instead
just present an HTML representation. There are two styles of HTML renderer
provided by REST framework, one for dealing with HTML rendered using
templates, the other for dealing with pre-rendered HTML. The second renderer
is the one we'd like to use for this endpoint.
"""

from rest_framework import renderers

# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
"""
REST framework includes an abstraction for dealing with ViewSets, that allows
the developer to concentrate on modeling the state and interactions of the
API, and leave the URL construction to be handled automatically, based on
common conventions.

ViewSet classes are almost the same thing as View classes, except that they
provide operations such as read, or update, and not method handlers such as
get or put.

A ViewSet class is only bound to a set of method handlers at the last moment,
when it is instantiated into a set of views, typically by using a Router
class which handles the complexities of defining the URL conf for you.

Let's take our current set of views, and refactor them into view sets.

First of all let's refactor our UserList and UserDetail views into a single
UserViewSet. We can remove the two views, and replace them with a single class:
"""

from rest_framework import viewsets


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

Next we're going to replace the SnippetList, SnippetDetail and
SnippetHighlight view classes. We can remove the three views, and again
replace them with a single class.
"""

from rest_framework.decorators import detail_route


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