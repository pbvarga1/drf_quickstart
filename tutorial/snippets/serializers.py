from rest_framework import serializers
from snippets.models import Snippet
from django.contrib.auth.models import User


"""
Dealing with relationships between entities is one of the more challenging
aspects of Web API design. There are a number of different ways that we might
choose to represent a relationship:

* Using primary keys.
* Using hyperlinking between entities.
* Using a unique identifying slug field on the related entity.
* Using the default string representation of the related entity.
* Nesting the related entity inside the parent representation.
* Some other custom representation.

REST framework supports all of these styles, and can apply them across
forward or reverse relationships, or apply them across custom managers such
as generic foreign keys.

In this case we'd like to use a hyperlinked style between entities. In order
to do so, we'll modify our serializers to extend HyperlinkedModelSerializer
instead of the existing ModelSerializer.

The HyperlinkedModelSerializer has the following differences from
ModelSerializer:

It does not include the pk field by default.
It includes a url field, using HyperlinkedIdentityField.
Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.
We can easily re-write our existing serializers to use hyperlinking.

Notice that we've also added a new 'highlight' field. This field is of the
same type as the url field, except that it points to the 'snippet-highlight'
url pattern, instead of the 'snippet-detail' url pattern.

Because we've included format suffixed URLs such as '.json', we also need to
indicate on the highlight field that any format suffixed hyperlinks it
returns should use the '.html' suffix.
"""


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets')
