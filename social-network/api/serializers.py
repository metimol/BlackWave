from rest_framework import serializers
from network.models import *


class ProfileSerializer(serializers.ModelSerializer):
    # Все поля из user кроме пароля
    id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    is_superuser = serializers.BooleanField(source="user.is_superuser", read_only=True)
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    last_login = serializers.DateTimeField(source="user.last_login", read_only=True)
    is_bot = serializers.BooleanField(source="user.is_bot", read_only=True)
    category = serializers.CharField(source="user.category", read_only=True)
    like_probability = serializers.FloatField(source="user.like_probability", read_only=True)
    comment_probability = serializers.FloatField(source="user.comment_probability", read_only=True)
    follow_probability = serializers.FloatField(source="user.follow_probability", read_only=True)
    unfollow_probability = serializers.FloatField(source="user.unfollow_probability", read_only=True)
    repost_probability = serializers.FloatField(source="user.repost_probability", read_only=True)
    following = serializers.SerializerMethodField()
    following_count = serializers.IntegerField(source="user.following_count", read_only=True)
    followers_count = serializers.IntegerField(source="user.followers_count", read_only=True)
    posts_count = serializers.IntegerField(source="user.posts_count", read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=True)
    category = serializers.CharField(source="user.category", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "is_bot",
            "category",
            "like_probability",
            "comment_probability",
            "follow_probability",
            "unfollow_probability",
            "repost_probability",
            "following",
            "following_count",
            "posts_count",
            "followers_count",
            "name",
            "image",
            "dob",
            "bio",
            "user_id",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "is_bot",
            "category",
            "like_probability",
            "comment_probability",
            "follow_probability",
            "unfollow_probability",
            "repost_probability",
            "following",
            "following_count",
            "posts_count",
            "followers_count",
        ]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id", None)
        if not user_id:
            raise serializers.ValidationError({"user_id": "user_id is required"})
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise serializers.ValidationError({"user_id": "User not found"})
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def get_following(self, obj):
        # No user, always False
        return False


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)
    bookmarked = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "date",
            "ispinned",
            "liked",
            "bookmarked",
            "reactions_count",
            "comments_count",
            "user",
            "user_id",
        ]
        read_only_fields = [
            "id",
            "date",
            "ispinned",
            "liked",
            "bookmarked",
            "reactions_count",
            "comments_count",
            "user",
        ]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id", None)
        if not user_id:
            raise serializers.ValidationError({"user_id": "user_id is required"})
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise serializers.ValidationError({"user_id": "User not found"})
        post = Post.objects.create(user=user, **validated_data)
        return post

    def get_user(self, obj) -> dict:
        user = obj.user
        return {
            "id": user.id,
            "username": user.username,
            "name": user.profile.name if user.profile else None,
            "image": (
                user.profile.image if user.profile and user.profile.image else None
            ),
        }

    def get_liked(self, obj) -> bool:
        # No user, always False
        return False

    def get_bookmarked(self, obj) -> bool:
        # No user, always False
        return False


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ["id", "content", "post", "date", "user", "user_id"]
        read_only_fields = ["id", "date", "user"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id", None)
        post = validated_data.get("post")
        if not user_id:
            raise serializers.ValidationError({"user_id": "user_id is required"})
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise serializers.ValidationError({"user_id": "User not found"})
        comment = Comment.objects.create(user=user, **validated_data)
        return comment

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "username": user.username,
            "name": user.profile.name if user.profile else None,
            "image": (
                user.profile.image if user.profile and user.profile.image else None
            ),
        }


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
