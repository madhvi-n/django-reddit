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

  constructor(private postService: PostService) { }

  ngOnInit(): void {
  }

  upvote() {
    if(this.post.user_vote){
      if(this.post.user_vote.vote == 1) {
        this.removeVote();
      } else {
        const current_vote = this.post.user_vote.vote += 1
        const data = {
          user: this.user_id,
          vote: current_vote
        }
        this.postService.updateVote(this.post.uuid, this.post.user_vote.id, data).subscribe(
          (response:any) => {
            this.post.user_vote = response;
            this.post.votes += response.vote;
          })
      }
    } else {
      const data = {
        user: this.user_id,
        vote: 1
      }
      this.postService.addVote(this.post.uuid, data).subscribe(
        (response: any) => {
          this.post.user_vote = response;
          this.post.votes += response.vote;
        })
    }
  }

  downvote() {
    if(this.post.user_vote) {
      if(this.post.user_vote.vote == -1) {
        this.removeVote();
      }
      const current = this.post.user_vote.vote -= 1
      const data = {
        user: this.user_id,
        vote: current
      }
      this.postService.updateVote(this.post.uuid, this.post.user_vote.id, data).subscribe(
        (response: any) => {
          this.post.user_vote = response;
          this.post.votes += response.vote;
        });
    } else {
      const data = {
        user: this.user_id,
        vote: -1
      }
      this.postService.addVote(this.post.uuid, data).subscribe(
        (response: any) => {
          this.post.user_vote = response;
          this.post.votes += response.vote;
        })
    }
  }

  removeVote() {
    if(!this.post.user_vote?.id) {
      return;
    }

    this.postService.deleteVote(this.post.uuid, this.post.user_vote.id).subscribe(
      (response: any) => {
        this.post.user_vote = null;
        // real time changes
      })
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
}
