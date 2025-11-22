import { Component, OnInit, Input } from '@angular/core';
import { User } from '@reddit/core/models/user.model';


@Component({
  selector: 'app-comment-user',
  templateUrl: './comment-user.component.html',
  styleUrls: ['./comment-user.component.scss']
})
export class CommentUserComponent implements OnInit {
  @Input() user: User;
  @Input() avatar_mode: boolean = false;
  @Input() header_mode: boolean = false;
  @Input() flair: string = 'User';
  @Input() is_removed = false;

  constructor() { }

  ngOnInit() {
  }

}
