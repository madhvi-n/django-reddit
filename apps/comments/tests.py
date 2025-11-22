import pytest
from unittest.mock import patch
from model_bakery import baker
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import PostComment, PostCommentVote
from comments.serializers import PostCommentCreateSerializer, PostCommentSerializer
from comments.services import add_mentioned_users, remove_users


# Model Tests
@pytest.mark.django_db
def test_post_comment_model_creation():
    """
    Test that a PostComment can be created successfully.
    """
    user = baker.make(User)
    post = baker.make(Post)
    comment = baker.make(
        PostComment, _comment="This is a test comment.", user=user, post=post
    )
    assert comment.pk is not None
    assert comment.comment == "This is a test comment."
    assert not comment.is_removed
    assert str(comment) == f"Comment: {comment.post.title} by {comment.user.username}"


@pytest.mark.django_db
def test_post_comment_is_removed():
    """
    Test the 'comment' property when a comment is marked as removed.
    """
    comment = baker.make(PostComment, is_removed=True)
    assert comment.comment == "This comment has been removed"


@pytest.mark.django_db
def test_post_comment_score_calculation():
    """
    Test the score calculation for a PostComment.
    """
    comment = baker.make(PostComment)
    baker.make(PostCommentVote, post_comment=comment, vote=1, _quantity=3)
    baker.make(PostCommentVote, post_comment=comment, vote=-1)
    assert comment.score == 2


@pytest.mark.django_db
def test_post_comment_vote_model_creation():
    """
    Test that a PostCommentVote can be created successfully.
    """
    vote = baker.make(PostCommentVote, vote=1)
    assert vote.pk is not None
    assert vote.vote == 1
    assert str(vote) == f"1 point by {vote.user.username}"


# Service Tests
@pytest.mark.django_db
def test_add_mentioned_users_service():
    """
    Test the add_mentioned_users service.
    """
    comment = baker.make(PostComment)
    user = baker.make(User)
    add_mentioned_users(user.pk, comment)
    assert user in comment.mentioned_users.all()


@pytest.mark.django_db
def test_remove_users_service():
    """
    Test the remove_users service.
    """
    user = baker.make(User)
    comment = baker.make(PostComment)
    comment.mentioned_users.add(user)
    remove_users(user.pk, comment)
    assert user not in comment.mentioned_users.all()


# Serializer Tests
@pytest.mark.django_db
def test_post_comment_create_serializer_valid():
    """
    Test that the PostCommentCreateSerializer can successfully create a comment.
    """
    user = baker.make(User)
    post = baker.make(Post)
    data = {
        "user": user.pk,
        "post": post.pk,
        "comment": "A valid test comment.",
    }
    serializer = PostCommentCreateSerializer(data=data)
    assert serializer.is_valid(raise_exception=True)
    comment = serializer.save()
    assert comment.user == user
    assert comment.post == post
    assert comment._comment == "A valid test comment."


# ViewSet Tests
@pytest.mark.django_db
class TestPostCommentViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = baker.make(User)
        self.post = baker.make(Post)
        self.url = reverse("post-comments-list", kwargs={"post_uuid": self.post.uuid})

    def test_list_comments(self):
        """
        Test listing comments for a post.
        """
        baker.make(PostComment, post=self.post, is_removed=False, _quantity=3)
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_create_comment_authenticated(self):
        """
        Test creating a comment for an authenticated user.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "user": self.user.pk,
            "comment": "A new test comment.",
            "post": self.post.pk,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 201
        assert response.data["comment"] == "A new test comment."

    @patch("comments.views.add_mentioned_users")
    def test_create_comment_with_mentions(self, mock_add_mentioned_users):
        """
        Test that the add_mentioned_users service is called when creating a comment with mentions.
        """
        self.client.force_authenticate(user=self.user)
        mentioned_user = baker.make(User)
        data = {
            "user": self.user.pk,
            "comment": "A comment mentioning @testuser",
            "mentioned_users": [mentioned_user.pk],
            "post": self.post.pk,
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == 201
        mock_add_mentioned_users.assert_called()

    def test_update_comment_by_owner(self):
        """
        Test that a user can update their own comment.
        """
        comment = baker.make(PostComment, user=self.user, post=self.post)
        self.client.force_authenticate(user=self.user)
        update_url = reverse(
            "post-comments-detail",
            kwargs={"post_uuid": self.post.uuid, "pk": comment.pk},
        )
        data = {
            "user": self.user.pk,
            "comment": "This comment has been updated.",
            "post": self.post.pk,
        }
        response = self.client.put(update_url, data)
        assert response.status_code == 200
        assert response.data["comment"] == "This comment has been updated."

    def test_delete_comment_by_owner(self):
        """
        Test that a user can delete their own comment (soft delete).
        """
        comment = baker.make(PostComment, user=self.user, post=self.post)
        self.client.force_authenticate(user=self.user)
        delete_url = reverse(
            "post-comments-detail",
            kwargs={"post_uuid": self.post.uuid, "pk": comment.pk},
        )
        response = self.client.delete(delete_url)
        assert response.status_code == 200
        comment.refresh_from_db()
        assert comment.is_removed

    def test_vote_actions(self):
        """
        Test upvote, downvote, and remove_vote actions on a comment.
        """
        comment = baker.make(PostComment, post=self.post)
        self.client.force_authenticate(user=self.user)

        # Upvote
        upvote_url = reverse(
            "post-comments-upvote",
            kwargs={"post_uuid": self.post.uuid, "pk": comment.pk},
        )
        response = self.client.put(upvote_url)
        assert response.status_code == 200
        assert response.data["vote"] == 1
        assert response.data["votes"] == 1

        # Downvote
        downvote_url = reverse(
            "post-comments-downvote",
            kwargs={"post_uuid": self.post.uuid, "pk": comment.pk},
        )
        response = self.client.put(downvote_url)
        assert response.status_code == 200
        assert response.data["vote"] == -1
        assert response.data["votes"] == -1

        # Remove vote
        remove_vote_url = reverse(
            "post-comments-remove-vote",
            kwargs={"post_uuid": self.post.uuid, "pk": comment.pk},
        )
        response = self.client.put(remove_vote_url)
        assert response.status_code == 200
        assert response.data["vote"] == 0
        assert response.data["votes"] == 0
