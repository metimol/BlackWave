from django.contrib import admin
from django.utils.html import format_html
from .models import User, Profile, Post, Comment

admin.site.index_title = "Welcome to the Cartouche Admin Panel"
admin.site.site_header = "Cartouche Social Network Administration"
admin.site.site_title = "Cartouche Admin"

# --- Real Users ---
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    fields = ("name", "image", "dob", "bio")
    extra = 0

class RealUserAdmin(admin.ModelAdmin):
    list_display = ("username", "profile_image", "is_active", "is_staff", "date_joined")
    search_fields = ("username",)
    list_filter = ("is_active", "is_staff", "date_joined")
    readonly_fields = ("date_joined",)
    inlines = [ProfileInline]
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_bot=False).select_related("profile")

    def profile_image(self, obj):
        if hasattr(obj, "profile") and obj.profile and obj.profile.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile.image,
            )
        return "No Image"
    profile_image.short_description = "Avatar"

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'add' in actions:
            del actions['add']
        return actions

# --- BotUser Proxy Model ---
class BotUser(User):
    class Meta:
        proxy = True
        verbose_name = "Bot"
        verbose_name_plural = "Bots"

# --- Bots ---
class BotProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Bot Profile"
    fk_name = "user"
    fields = ("name", "image", "dob", "bio")
    extra = 0

class BotUserAdmin(admin.ModelAdmin):
    list_display = ("username", "profile_image", "category", "gender", "date_joined")
    search_fields = ("username", "category")
    list_filter = ("category", "gender", "date_joined")
    readonly_fields = ("date_joined", "username", "category", "gender", "profile_image")
    inlines = [BotProfileInline]
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_bot=True).select_related("profile")

    def profile_image(self, obj):
        if hasattr(obj, "profile") and obj.profile and obj.profile.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile.image,
            )
        return "No Image"
    profile_image.short_description = "Avatar"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'add' in actions:
            del actions['add']
        if 'change' in actions:
            del actions['change']
        return actions

# --- Posts ---
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("short_content", "user", "date", "reactions_count", "comments_count")
    search_fields = ("content", "user__username")
    list_filter = ("date",)
    readonly_fields = ("reactions_count", "comments_count")
    list_per_page = 20

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "Post"

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'add' in actions:
            del actions['add']
        return actions

# --- Comments ---
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "short_content", "post", "date")
    search_fields = ("user__username", "content")
    list_filter = ("date",)
    list_per_page = 20

    def short_content(self, obj):
        return obj.content[:40] + "..." if len(obj.content) > 40 else obj.content
    short_content.short_description = "Comment"

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'add' in actions:
            del actions['add']
        return actions

admin.site.register(User, RealUserAdmin)
admin.site.register(BotUser, BotUserAdmin)