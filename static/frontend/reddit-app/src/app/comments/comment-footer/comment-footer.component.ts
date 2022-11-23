import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommentService } from '@reddit/core/services/comment/comment.service';
import { User } from '@reddit/core/models/user.model';
import { Comment } from '@reddit/core/models/comment.model';


@Component({
  selector: 'app-comment-footer',
  templateUrl: './comment-footer.component.html',
  styleUrls: ['./comment-footer.component.scss']
})
export class CommentFooterComponent implements OnInit {
  @Input() comment: Comment;
  @Input() user: User;
  @Input() uuid: string;
  @Input() nested = true;
  @Output() mention = new EventEmitter<any>();
  @Output() nestedReply = new EventEmitter<any>();
  can_reply: boolean = true;
  nestedReplyFlag: boolean = false;
  user_vote = 0;

  constructor(private commentService: CommentService
  ) { }

  ngOnInit() {
    if (this.user.id == this.comment.user.id) {
      this.can_reply = false;
    }
    this.checkUserVote();
  }

  checkUserVote(){
    this.commentService.checkUserVote(this.uuid, this.comment.id).subscribe(
      (response) => {
        console.log(response);
        this.setVoteData(response);
      })
  }

  setVoteData(response) {
    this.user_vote = response?.vote;
    this.comment.votes = response?.votes;
  }

  upvoteClicked() {
    if (this.comment.is_removed) {
      return;
    }
    if (this.user_vote == 1) {
      this.removeVote();
    } else {
      this.upvoteComment();
    }
  }

  downvoteClicked() {
    if (this.comment.is_removed) {
      return;
    }
    if (this.user_vote == -1) {
      this.removeVote();
    } else {
      this.downvoteComment();
    }
  }

  upvoteComment() {
    this.commentService.upvoteComment(this.uuid, this.comment.id).subscribe(
      (response: any) => {
        this.setVoteData(response);
      }, (err) => {
        console.log(err);
      }
    );
  }

  removeVote() {
    this.commentService.removeVote(this.uuid, this.comment.id).subscribe(
      (response) => {
        this.setVoteData(response);
      }, (err) => {
        console.log(err);
      }
    );
  }

  downvoteComment() {
    this.commentService.downvoteComment(this.uuid, this.comment.id).subscribe(
      (response) => {
        console.log(response);
        this.setVoteData(response);
      }, (err) => {
        console.log(err);
      }
    );
  }

  mentionUser() {
    this.mention.emit(this.comment.user);
  }

  nestedReplyEvent() {
    this.nestedReply.emit(true);
  }
}
