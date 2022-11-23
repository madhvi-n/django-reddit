import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Comment } from '@reddit/core/models/comment.model';
import { User } from '@reddit/core/models/user.model';


@Component({
  selector: 'app-comment-list',
  templateUrl: './comment-list.component.html',
  styleUrls: ['./comment-list.component.scss']
})
export class CommentListComponent implements OnInit {
  @Input() comments: Comment[] = [];
  @Input() user: User;
  @Input() uuid: string;
  @Output() mentioned = new EventEmitter<any>();
  @Input() max_nest_depth: number = 0;
  @Input() current_nest_depth: number = 0;

  constructor() { }

  ngOnInit() {
    // console.log(this.comments, "list");
  }

  removed(removed_comment: any) {
    this.comments.map((comment, index) => {
      if (comment.id == removed_comment.id) {
        this.comments.splice(index, 1);
      }
    });
  }

  hightlight(data: any) {
    // console.log(data, "Highlight event");
  }

  userMentioned(data: any) {
    console.log(data);
    this.mentioned.emit(data);
  }

}
