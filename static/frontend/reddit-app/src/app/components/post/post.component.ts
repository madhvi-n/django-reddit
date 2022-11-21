import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Post } from '@reddit/core/models/post.model';
import { PostService } from '@reddit/core/services/post/post.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit {
  @Input() post: Post;
  @Input() user_id: number;
  user_vote = 0;

  constructor(private postService: PostService) { }

  ngOnInit(): void {
    this.user_vote = this.post?.user_vote?.vote;
  }

  upvoteClicked(){
    if (this.user_vote == 1) {
      this.removeVote();
    } else {
      this.upvote();
    }
  }

  downvoteClicked(){
    if (this.user_vote == -1) {
      this.removeVote();
    } else {
      this.downvote();
    }
  }

  upvote() {
    this.postService.upvotePost(this.post.uuid).subscribe(
      (response: any) => {
        this.setVoteData(response);
      }, (err) => {
        console.log(err);
      }
    );
  }

  downvote(){
    this.postService.downvotePost(this.post.uuid).subscribe(
      (response) => {
        this.setVoteData(response);
      }, (err) => {
        console.log(err);
      }
    );
  }

  removeVote() {
    this.postService.removePostVote(this.post.uuid).subscribe(
      (response) => {
        this.setVoteData(response);
      }, (err) => {
        console.log(err);
      }
    );
  }

  setVoteData(response) {
    this.user_vote = response?.vote;
    this.post.votes = response?.votes;
  }

  checkBookmark() {
    if(this.post.user_bookmark) {
      this.removeBookmark();
    } else {
      this.addBookmark();
    }
  }

  removeBookmark() {
    this.postService.removeBookmark(this.post.uuid, this.post.user_bookmark.id).subscribe(
      (response: any) => {
        this.post.user_bookmark = null;
      },
      (err) => {
        console.log(err);
      });
  }

  addBookmark() {
    const data = {
      user: this.user_id
    }
    this.postService.addBookmark(this.post.uuid, data).subscribe(
      (response: any) => {
        this.post.user_bookmark = response;
      },
      (err) => {
        console.log(err);
      });
  }

  sharePost(uuid: string) {

  }
}
