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
  vote = 0;
  total = 0;

  constructor(private commentService: CommentService
  ) { }

  ngOnInit() {
    this.checkUserVote();
    if (this.user.id == this.comment.user.id) {
      this.can_reply = false;
    }
    if (this.user.id !== this.comment.user.id) {
      this.can_reply = true;
    }
  }

  checkUserVote() {
    // if (this.comment.is_removed) {
    //   return;
    // }
  }

  setVoteData(response) {
    this.vote = response.vote;
    this.total = response.votes;
  }

  upvoteClicked() {
    if (this.comment.is_removed) {
      return;
    }
    if (this.vote == 1) {
      this.removeVote();
    } else {
      this.upvoteComment();
    }
  }

  downvoteClicked() {
    if (this.comment.is_removed) {
      return;
    }
    if (this.vote == -1) {
      this.removeVote();
    } else {
      this.downvoteComment();
    }
  }

  upvoteComment() {
    // this.commentService.upvoteComment(this.uuid, this.comment.id, this.user.id).subscribe(
    //   (response: any) => {
    //     // console.log(response);
    //     this.setVoteData(response);
    //   }, (err) => {
    //     console.log(err);
    //   }
    // );
  }

  removeVote() {
    // this.commentService.removeCommentVote(this.uuid, this.comment.id, this.comment.vote.id).subscribe(
    //   (response) => {
    //     this.setVoteData(response);
    //   }, (err) => {
    //     console.log(err);
    //   }
    // );
  }

  downvoteComment() {
    // this.commentService.downvoteComment(this.uuid, this.comment.id, this.user.id).subscribe(
    //   (response) => {
    //     this.setVoteData(response);
    //   }, (err) => {
    //     console.log(err);
    //   }
    // );
  }

  mentionUser() {
    this.mention.emit(this.comment.user);
  }

  nestedReplyEvent() {
    this.nestedReply.emit(true);
  }
}
