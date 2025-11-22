import pytest
from model_bakery import baker
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from posts.models import Post


@pytest.mark.django_db
def test_post_follower_creation():
    """Test creating a post follower."""
    follower = baker.make("followers.PostFollower")
    assert follower.id is not None


@pytest.mark.django_db
def test_user_follower_creation():
    """Test creating a user follower."""
    follower = baker.make("followers.UserFollower")
    assert follower.id is not None


@pytest.mark.django_db
class TestPostFollowerViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = baker.make(User)
        self.post = baker.make(Post)
        self.url = reverse("post-followers-list", kwargs={"post_uuid": self.post.uuid})

    def test_forbidden_methods(self):
        """Test that list, retrieve, update, and partial_update are forbidden."""
        url_detail = reverse(
            "post-followers-detail", kwargs={"post_uuid": self.post.uuid, "pk": 1}
        )
        response_list = self.client.get(self.url)
        response_retrieve = self.client.get(url_detail)
        response_update = self.client.put(url_detail, {})
        response_partial_update = self.client.patch(url_detail, {})

        assert response_list.status_code == 403
        assert response_retrieve.status_code == 403
        assert response_update.status_code == 403
        assert response_partial_update.status_code == 403

    def test_create_post_follower(self):
        """Test creating a post follower."""
        self.client.force_authenticate(user=self.user)
        data = {"follower": self.user.pk, "post": self.post.pk}
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == 201

    def test_destroy_post_follower(self):
        """Test deleting a post follower."""
        follower = baker.make(
            "followers.PostFollower", follower=self.user, post=self.post
        )
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "post-followers-detail",
            kwargs={"post_uuid": self.post.uuid, "pk": follower.pk},
        )
        response = self.client.delete(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserFollowerViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = baker.make(User)
        self.followed_user = baker.make(User)
        self.url = reverse(
            "user-followers-list", kwargs={"user_pk": self.followed_user.pk}
        )

    def test_forbidden_methods(self):
        """Test that list, retrieve, update, and partial_update are forbidden."""
        url_detail = reverse(
            "user-followers-detail",
            kwargs={"user_pk": self.followed_user.pk, "pk": 1},
        )
        response_list = self.client.get(self.url)
        response_retrieve = self.client.get(url_detail)
        response_update = self.client.put(url_detail, {})
        response_partial_update = self.client.patch(url_detail, {})

        assert response_list.status_code == 403
        assert response_retrieve.status_code == 403
        assert response_update.status_code == 403
        assert response_partial_update.status_code == 403

    def test_create_user_follower(self):
        """Test creating a user follower."""
        self.client.force_authenticate(user=self.user)
        data = {"follower": self.user.pk}  # follower is the authenticated user
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == 201
        assert response.data["follower"] == self.user.pk

    def test_destroy_user_follower(self):
        """Test deleting a user follower."""
        follower = baker.make(
            "followers.UserFollower",
            follower=self.user,
            followed_user=self.followed_user,
        )
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "user-followers-detail",
            kwargs={"user_pk": self.followed_user.pk, "pk": follower.pk},
        )
        response = self.client.delete(url)
        assert response.status_code == 200
