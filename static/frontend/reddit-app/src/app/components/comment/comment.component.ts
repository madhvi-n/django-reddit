import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { UserService } from '@reddit/core/services/user/user.service';
import { CommentService } from '@reddit/core/services/comment/comment.service';
import { MatDialog } from '@angular/material/dialog';
import { User } from '@reddit/core/models/user.model';
import { Comment } from '@reddit/core/models/comment.model';
import { ConfirmationDialogComponent } from '../confirmation-dialog/confirmation-dialog.component';


@Component({
  selector: 'app-comment',
  templateUrl: './comment.component.html',
  styleUrls: ['./comment.component.scss']
})
export class CommentComponent implements OnInit {
  @Input() comment: Comment;
  @Input() user: User;
  @Input() uuid: string;
  @Input() nested: boolean = true;
  @Input() max_nested_depth: number = 0;
  @Input() current_nest_depth: number = 0;
  can_edit: boolean = false;
  edit_mode: boolean = false;
  nested_reply_event: boolean = false;
  expanded: boolean = false;

  @Output() removed = new EventEmitter<Comment>();
  @Output() mentioned = new EventEmitter<any>();

  constructor(
    private userService: UserService,
    private commentService: CommentService,
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
  this.getAuthUser();
}

  getAuthUser() {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if (initialized) {
          this.userService.user.subscribe(
            (user: User) => {
              this.user = user;
              this.checkAuthUser();
            }
          );
        }
      }
    );
  }

  checkAuthUser() {
    if (this.comment.user.id === this.user.id) {
      this.can_edit = true;
    }
  }

  toggle() {
    this.expanded = !this.expanded;
  }

  nestedReplyEvent(event) {
    this.nested_reply_event = event;
  }

  editComment() {
    this.edit_mode = true;
  }

  commentEditted(data: any) {
    this.comment = data;
    this.edit_mode = false;
  }

  userMentioned(data: any) {
    // console.log(data);
    this.mentioned.emit(data);
  }

  removeComment(comment) {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '380px',
      height: '200px',
      data: {
        message: `Are you sure you want to
          delete this comment?`,
        okayButtonText: 'Yes'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.commentService.removeComment(this.uuid, comment.id).subscribe(
          (response) => {
            // console.log(response);
            if (comment.child_count === 0) {
              this.removed.emit(comment);
            } else {
              comment.comment = 'This comment has been removed';
              comment.is_removed = true;
            }
          }, (err) => {
            console.log(err);
          });
      } else {

      }
    });
  }
}
