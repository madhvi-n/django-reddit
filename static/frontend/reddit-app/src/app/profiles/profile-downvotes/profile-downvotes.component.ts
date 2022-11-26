import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { CommentService } from '@reddit/core/services/comment/comment.service';
import { GroupService } from '@reddit/core/services/group/group.service';
import { User } from '@reddit/core/models/user.model';
import { Group } from '@reddit/core/models/group.model';
import { UserComment } from '@reddit/core/models/comment.model';

@Component({
  selector: 'app-profile-downvotes',
  templateUrl: './profile-downvotes.component.html',
  styleUrls: ['./profile-downvotes.component.scss']
})
export class ProfileDownvotesComponent implements OnInit {
  isLoading: boolean = false;
  @Input() user: User;
  downvotes = [];

  constructor(
    private userService: UserService,
    private groupService: GroupService,
    private commentService: CommentService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.getUserDownvotes();
  }

  getUserDownvotes() {
    this.userService.userDownvotes(this.user.username).subscribe(
      (response: any) => {
        const data = [...response.posts, ...response.comments];
        this.downvotes = data.sort((a, b) => b.created_at - a.created_at);
        console.log(this.downvotes);
      });
  }
}
