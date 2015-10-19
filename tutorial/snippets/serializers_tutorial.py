from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


# class SnippetSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(
#         required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(
#         choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES,default='friendly')

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated
#         data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

"""
Our SnippetSerializer class is replicating a lot of information that's also
contained in the Snippet model. It would be nice if we could keep our code a
bit more concise.
It's important to remember that ModelSerializer classes don't do anything
particularly magical, they are simply a shortcut for creating serializer
classes:

    * An automatically determined set of fields.
    * Simple default implementations for the create() and update() methods.
"""


# class SnippetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Snippet
#         fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
#         owner = serializers.ReadOnlyField(source='owner.username')


# class UserSerializer(serializers.ModelSerializer):
#     snippets = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Snippet.objects.all())

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'snippets')


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
