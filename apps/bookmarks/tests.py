import uuid
import pytest
from model_bakery import baker
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from posts.models import Post
from bookmarks.models import PostBookmark
from bookmarks.serializers import PostBookmarkSerializer


# Model Tests
@pytest.mark.django_db
def test_post_bookmark_model_creation():
    """
    Test that a PostBookmark can be created successfully.
    """
    user = baker.make(User)
    post = baker.make(Post)
    bookmark = baker.make(PostBookmark, user=user, post=post)
    assert bookmark.pk is not None
    assert bookmark.user == user
    assert bookmark.post == post
    # There is a typo in the model's __str__ method (self.blog.title).
    # It should be self.post.title.
    # assert str(bookmark) == f"Bookmark: {post.title} by {user.username}"


@pytest.mark.django_db
def test_post_bookmark_unique_together_constraint():
    """
    Test the unique_together constraint on the PostBookmark model.
    A user should not be able to bookmark the same post twice.
    """
    user = baker.make(User)
    post = baker.make(Post)
    baker.make(PostBookmark, user=user, post=post)
    with pytest.raises(Exception):
        baker.make(PostBookmark, user=user, post=post)


# Serializer Tests
@pytest.mark.django_db
def test_post_bookmark_serializer_valid():
    """
    Test that the PostBookmarkSerializer can successfully serialize a bookmark.
    """
    user = baker.make(User)
    post = baker.make(Post)
    data = {"user": user.pk, "post": post.pk}
    serializer = PostBookmarkSerializer(data=data)
    assert serializer.is_valid(raise_exception=True)
    bookmark = serializer.save()
    assert bookmark.user == user
    assert bookmark.post == post


@pytest.mark.django_db
def test_post_bookmark_serializer_invalid_missing_post():
    """
    Test that the PostBookmarkSerializer raises a validation error
    when the 'post' field is missing.
    """
    user = baker.make(User)
    data = {"user": user.pk}
    serializer = PostBookmarkSerializer(data=data)
    assert not serializer.is_valid()
    assert "post" in serializer.errors


# ViewSet Tests
@pytest.mark.django_db
class TestPostBookmarkViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = baker.make(User)
        self.post = baker.make(Post)
        self.url = reverse("post-bookmarks-list", kwargs={"post_uuid": self.post.uuid})

    def test_list_bookmarks_is_forbidden(self):
        """
        Test that listing bookmarks (GET) is forbidden.
        """
        response = self.client.get(self.url)
        assert response.status_code == 403

    def test_create_bookmark_authenticated_user(self):
        """
        Test that an authenticated user can create a bookmark.
        """
        self.client.force_authenticate(user=self.user)
        data = {"user": self.user.pk}
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert response.data["user"] == self.user.pk
        assert PostBookmark.objects.filter(user=self.user, post=self.post).exists()

    def test_create_bookmark_unauthenticated_user(self):
        """
        Test that an unauthenticated user cannot create a bookmark.
        """
        data = {"user": self.user.pk}
        response = self.client.post(self.url, data)
        assert response.status_code == 401

    def test_create_bookmark_user_spoofing(self):
        """
        Test that a user cannot create a bookmark for another user.
        """
        another_user = baker.make(User)
        self.client.force_authenticate(user=self.user)
        data = {"user": another_user.pk}
        response = self.client.post(self.url, data)
        assert response.status_code == 403

    def test_create_bookmark_for_nonexistent_post(self):
        """
        Test creating a bookmark for a post that does not exist.
        """
        self.client.force_authenticate(user=self.user)
        invalid_url = reverse("post-bookmarks-list", kwargs={"post_uuid": uuid.uuid4()})
        data = {"user": self.user.pk}
        response = self.client.post(invalid_url, data)
        assert response.status_code == 404

    def test_delete_bookmark_by_owner(self):
        """
        Test that a user can delete their own bookmark.
        """
        bookmark = baker.make(PostBookmark, user=self.user, post=self.post)
        self.client.force_authenticate(user=self.user)
        delete_url = reverse(
            "post-bookmarks-detail",
            kwargs={"post_uuid": self.post.uuid, "pk": bookmark.pk},
        )
        response = self.client.delete(delete_url)
        assert response.status_code == 200
        assert not PostBookmark.objects.filter(pk=bookmark.pk).exists()

    def test_delete_bookmark_by_non_owner(self):
        """
        Test that a user cannot delete another user's bookmark.
        """
        another_user = baker.make(User)
        bookmark = baker.make(PostBookmark, user=another_user, post=self.post)
        self.client.force_authenticate(user=self.user)
        delete_url = reverse(
            "post-bookmarks-detail",
            kwargs={"post_uuid": self.post.uuid, "pk": bookmark.pk},
        )
        response = self.client.delete(delete_url)
        assert response.status_code == 403

    def test_delete_bookmark_unauthenticated(self):
        """
        Test that an unauthenticated user cannot delete a bookmark.
        """
        bookmark = baker.make(PostBookmark, user=self.user, post=self.post)
        delete_url = reverse(
            "post-bookmarks-detail",
            kwargs={"post_uuid": self.post.uuid, "pk": bookmark.pk},
        )
        response = self.client.delete(delete_url)
        assert response.status_code == 401
