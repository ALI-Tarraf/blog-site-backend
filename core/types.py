from graphene_django import DjangoObjectType
from .models import Post, Category, Tag, Comment, Profile
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["id", "username", "profile"]


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "category",
            "tags",
            "created_at",
            "updated_at",
        ]


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ["id", "content", "author", "post", "created_at"]


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ["id", "bio", "location", "website", "created_at"]
