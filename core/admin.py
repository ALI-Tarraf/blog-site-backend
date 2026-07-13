from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Category, Tag, Comment, Profile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "created_at"]
    filter_horizontal = ["tags"]  # ← nice UI for ManyToMany in admin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "created_at"]


from .models import Post, Category, Tag, Comment, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "location", "website"]
