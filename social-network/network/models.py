from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_bot = models.BooleanField(default=False)
    category = models.CharField(max_length=100, default="", blank=True)
    like_probability = models.FloatField(default=0.5)
    comment_probability = models.FloatField(default=0.5)
    follow_probability = models.FloatField(default=0.5)
    unfollow_probability = models.FloatField(default=0.5)
    repost_probability = models.FloatField(default=0.5)
    gender = models.CharField(max_length=10, default="Male")
    prompt = models.TextField(default="", blank=True)

    @property
    def followers_list(self):
        return [connection.follower for connection in self.followers.all()]

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_list(self):
        return [connection.user for connection in self.following.all()]

    @property
    def following_count(self):
        return self.following.count()

    @property
    def posts_count(self):
        return self.posts.count()

    @property
    def liked_posts(self):
        reactions = Reaction.objects.filter(user=self)
        return [reaction.post for reaction in reactions]

    @property
    def bookmarked_posts(self):
        bookmarks = self.bookmarks.all().order_by("-date")
        posts = [bookmark.post for bookmark in bookmarks]
        return posts

    def __str__(self):
        return f"{self.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    image = models.URLField(blank=False, null=False)
    dob = models.DateField(blank=False, null=False)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} -> {self.name}"


class Connection(models.Model):
    user = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} followed by {self.follower}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "follower"], name="unique connection"
            )
        ]


class Post(models.Model):
    user = models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE, blank=False, null=False
    )
    content = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    ispinned = models.BooleanField(default=False)

    @property
    def reactions_count(self):
        return self.reactions.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.user}: {self.content[:25]}"


class Reaction(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="reactions",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.post}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique reaction")
        ]


class Comment(models.Model):
    content = models.TextField(blank=False, null=False)
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE, blank=False, null=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented {self.content} on {self.post}"


class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(
        User,
        related_name="bookmarks",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.post}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique bookmark")
        ]
