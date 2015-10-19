from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.conf.urls import include

# urlpatterns = [
#     url(r'^snippets/$', views.SnippetList.as_view()),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
#     url(r'^users/$', views.UserList.as_view()),
#     url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

# urlpatterns += [
#     url(r'^api-auth/', include('rest_framework.urls',
#                                namespace='rest_framework')),
#     url(r'^$', views.api_root),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
#         views.SnippetHighlight.as_view()),
# ]


""""
Making sure our URL Patterns are named
--------------------------------------
If we're going to have a hyperlinked API, we need to make sure we name our
URL patterns. Let's take a look at which URL patterns we need to name.

* The root of our API refers to 'user-list' and 'snippet-list'.
* Our snippet serializer includes a field that refers to 'snippet-highlight'.
* Our user serializer includes a field that refers to 'snippet-detail'.
* Our snippet and user serializers include 'url' fields that by default will
  refer to '{model_name}-detail', which in this case will be 'snippet-detail'
  and 'user-detail'.
"""

# # API endpoints
# urlpatterns = format_suffix_patterns([
#     url(r'^$', views.api_root),
#     url(r'^snippets/$',
#         views.SnippetList.as_view(),
#         name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$',
#         views.SnippetDetail.as_view(),
#         name='snippet-detail'),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
#         views.SnippetHighlight.as_view(),
#         name='snippet-highlight'),
#     url(r'^users/$',
#         views.UserList.as_view(),
#         name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$',
#         views.UserDetail.as_view(),
#         name='user-detail')
# ])

# # Login and logout views for the browsable API
# urlpatterns += [
#     url(r'^api-auth/', include('rest_framework.urls',
#                                namespace='rest_framework')),
# ]

"""
Binding ViewSets to URLs explicitly
-----------------------------------

The handler methods only get bound to the actions when we define the URLConf.
To see what's going on under the hood let's first explicitly create a set of
views from our ViewSets.

In the urls.py file we bind our ViewSet classes into a set of concrete views.

Notice how we're creating multiple views from each ViewSet class, by binding
the http methods to the required action for each view.
"""

from snippets.views import SnippetViewSet, UserViewSet
from rest_framework import renderers

# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })

"""
Now that we've bound our resources into concrete views, we can register the
views with the URL conf as usual.
"""
# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^snippets/$', snippet_list, name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight,
#         name='snippet-highlight'),
#     url(r'^users/$', user_list, name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
# ])

"""
Using Routers
-------------
Because we're using ViewSet classes rather than View classes, we actually
don't need to design the URL conf ourselves. The conventions for wiring up
resources into views and urls can be handled automatically, using a Router
class. All we need to do is register the appropriate view sets with a
router, and let it do the rest.

Registering the viewsets with the router is similar to providing a
urlpattern. We include two arguments - the URL prefix for the views, and the
viewset itself.

The DefaultRouter class we're using also automatically creates the API
root view for us, so we can now delete the api_root method from our views
module.
"""

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
