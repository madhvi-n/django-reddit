import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { User } from '@reddit/core/models/user.model';
import { Comment } from '@reddit/core/models/comment.model';
import { CommentService } from '@reddit/core/services/comment/comment.service';


@Component({
  selector: 'app-comment-edit',
  templateUrl: './comment-edit.component.html',
  styleUrls: ['./comment-edit.component.scss']
})
export class CommentEditComponent implements OnInit {
  @Input() user: User;
  @Input() uuid: string;
  @Input() new: boolean = true;
  @Input() comment_obj: Comment;
  @Input() mentioned_users: Set<any>;
  @Input() nested = false;
  @Input() parent: number;
  @Input() child_group = false;

  @Output() comment_response = new EventEmitter<Comment>();
  @Output() remove_mention = new EventEmitter<any>();
  @Output() clear_comment = new EventEmitter<any>();

  mentioned_user_ids = [];
  comment_loading = false;
  commentForm: FormGroup;

  constructor(private commentService: CommentService
  ) { }

  ngOnInit() {
    this.initiateCommentForm();
    // console.log(this.source, "comment-create");
  }

  get f() { return this.commentForm.controls; }

  initiateCommentForm() {
    let comment_string: String = '';
    if (this.comment_obj) {
      comment_string = this.comment_obj.comment;
    }

    this.commentForm = new FormGroup({
      comment: new FormControl(comment_string, {
        validators: [Validators.required, Validators.minLength(2), Validators.maxLength(2000)]
      })
    });
    // console.log(this.mentioned_users);
  }

  submit() {
    if (this.commentForm.invalid) {
      return;
    }
    let id = null;
    if (!this.new) {
      id = this.comment_obj.id;
    }

    if (
      this.new &&
      this.mentioned_users &&
      this.mentioned_users.size > 0
    ) {
      this.mentioned_users.forEach(
        (user) => {
          this.mentioned_user_ids.push(user.id);
        });
    }
    // console.log(this.mentioned_user_ids);

    let comment = {
      id: id,
      comment: this.commentForm.value.comment,
      user: this.user.id,
      mentioned_users: this.mentioned_user_ids,
      is_nesting_permitted: this.nested
    }

    if (this.child_group) {
      comment['parent'] = this.parent;
    }

    if (this.new) {
      this.createComment(comment);
    } else {
      this.updateComment(comment);
    }
  }

  cancel() {
    if (this.new) {
      this.commentForm.reset(this.commentForm.value.comment);
      this.clear_comment.emit(true);
    } else {
      this.comment_response.emit(this.comment_obj);
    }
  }


  createComment(comment) {
    this.commentForm.reset(this.commentForm.value.comment);
    this.clear_comment.emit(true);
    this.comment_loading = true;
    // console.log(this.source);

    this.commentService.createComment(this.uuid, comment).subscribe(
      (response: Comment) => {
        this.comment_loading = false;
        // console.log(response);
        this.comment_response.emit(response);
        this.clear_comment.emit(true);
        this.mentioned_user_ids.length = 0;
      }, (err) => {
        console.log(err);
        // this.commentForm.reset(this.commentForm.value.comment);
        this.comment_loading = false;
      }
    )
  }

  updateComment(comment) {
    this.commentService.updateComment(this.uuid, comment.id, comment).subscribe(
      (response: Comment) => {
        // console.log(response);
        this.comment_response.emit(response);
      }, (err) => {
        console.log(err);
      })
  }

  removeMention(user) {
    this.remove_mention.emit(user);
  }
}
