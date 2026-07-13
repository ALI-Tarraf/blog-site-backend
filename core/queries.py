import graphene
from .models import Post, Category, Tag, Comment, Profile
from .types import PostType, CategoryType, TagType, CommentType, ProfileType, UserType
from django.contrib.auth.models import User


class Query(graphene.ObjectType):

    all_posts = graphene.List(
        PostType,
        search=graphene.String(),
        ordering=graphene.String(),
        category_id=graphene.Int(),  # ← filter by category
        tag=graphene.String(),  # ← filter by tag name
    )

    post = graphene.Field(PostType, id=graphene.Int(required=True))
    all_categories = graphene.List(CategoryType)
    all_tags = graphene.List(TagType)
    post_comments = graphene.List(CommentType, post_id=graphene.Int(required=True))
    profile = graphene.Field(ProfileType, username=graphene.String(required=True))
    me = graphene.Field(UserType)
    # user posts
    user_posts = graphene.List(PostType, username=graphene.String(required=True))

    def resolve_all_posts(
        root, info, search=None, ordering=None, category_id=None, tag=None
    ):
        posts = Post.objects.all()

        if search:
            posts = posts.filter(title__icontains=search)

        if category_id:
            posts = posts.filter(category__id=category_id)

        if tag:
            posts = posts.filter(tags__name__icontains=tag)

        if ordering == "oldest":
            posts = posts.order_by("created_at")
        else:
            posts = posts.order_by("-created_at")

        return posts

    def resolve_post(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_tags(root, info):
        return Tag.objects.all()

    def resolve_post_comments(root, info, post_id):
        return Comment.objects.filter(post__id=post_id).order_by("-created_at")

    def resolve_profile(root, info, username):
        try:
            user = User.objects.get(username=username)
            return user.profile
        except User.DoesNotExist:
            return None

    def resolve_me(root, info):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in")
        return user

    def resolve_user_posts(root, info, username):
        try:
            user = User.objects.get(username=username)
            return Post.objects.filter(author=user)
        except User.DoesNotExist:
            return []
