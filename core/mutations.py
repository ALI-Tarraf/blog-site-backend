import graphene
from .models import Post, Category, Tag, Comment, Profile
from .types import PostType, CategoryType, TagType, CommentType, ProfileType
from django.core.cache import cache


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    category = graphene.Field(CategoryType)
    success = graphene.Boolean()

    def mutate(root, info, name, description=""):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in")
        category = Category.objects.create(name=name, description=description)
        return CreateCategory(category=category, success=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        category_id = graphene.Int()  # ← optional
        tag_ids = graphene.List(graphene.Int)  # ← optional list of tag ids

    post = graphene.Field(PostType)
    success = graphene.Boolean()

    def mutate(root, info, title, content, category_id=None, tag_ids=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in to create a post")

        category = None
        if category_id:
            try:
                category = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                raise Exception("Category not found")

        post = Post.objects.create(
            title=title, content=content, author=user, category=category
        )

        if tag_ids:
            tags = Tag.objects.filter(pk__in=tag_ids)
            post.tags.set(tags)  # ← ManyToMany uses .set()
        cache.clear()

        return CreatePost(post=post, success=True)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()
        category_id = graphene.Int()
        tag_ids = graphene.List(graphene.Int)

    post = graphene.Field(PostType)
    success = graphene.Boolean()

    def mutate(
        root, info, id, title=None, content=None, category_id=None, tag_ids=None
    ):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in")

        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        if post.author != user:
            raise Exception("You can only edit your own posts")

        if title:
            post.title = title
        if content:
            post.content = content
        if category_id:
            try:
                post.category = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                raise Exception("Category not found")
        if tag_ids is not None:
            tags = Tag.objects.filter(pk__in=tag_ids)
            post.tags.set(tags)

        post.save()
        cache.clear()
        return UpdatePost(post=post, success=True)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(root, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in")
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        if post.author != user:
            raise Exception("You can only delete your own posts")
        post.delete()
        cache.clear()
        return DeletePost(success=True, message="Post deleted successfully")


class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    success = graphene.Boolean()

    def mutate(root, info, post_id, content):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        comment = Comment.objects.create(post=post, author=user, content=content)
        return CreateComment(comment=comment, success=True)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in")
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            raise Exception("Comment not found")
        if comment.author != user:
            raise Exception("You can only delete your own comments")
        comment.delete()
        return DeleteComment(success=True)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        bio = graphene.String()
        location = graphene.String()
        website = graphene.String()

    profile = graphene.Field(ProfileType)
    success = graphene.Boolean()

    def mutate(root, info, bio=None, location=None, website=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You must be logged in")

        profile = user.profile
        if bio is not None:
            profile.bio = bio
        if location is not None:
            profile.location = location
        if website is not None:
            profile.website = website
        profile.save()
        return UpdateProfile(profile=profile, success=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_category = CreateCategory.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()
    update_profile = UpdateProfile.Field()
