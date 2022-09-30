import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Comment } from '@reddit/core/models/comment.model';
import { User } from '@reddit/core/models/user.model';

@Component({
  selector: 'app-comment-create',
  templateUrl: './comment-create.component.html',
  styleUrls: ['./comment-create.component.scss']
})
export class CommentCreateComponent implements OnInit {
  @Input() user: User;
  @Input() uuid: string;
  @Input() nested: boolean;
  @Input() parent: number;
  @Input() child_group = false;
  @Input() mentioned_users: Set<any>;

  @Output() comment_response = new EventEmitter<Comment>()
  @Output() remove_mention = new EventEmitter<any>()
  @Output() clear_comment = new EventEmitter<any>()

  constructor() { }

  ngOnInit() {

  }

  emitComment(data: any) {
    this.comment_response.emit(data);
  }

  removeMention(data: any) {
    this.remove_mention.emit(data);
  }

  clearComment(data: any) {
    this.clear_comment.emit(data);
  }
}
