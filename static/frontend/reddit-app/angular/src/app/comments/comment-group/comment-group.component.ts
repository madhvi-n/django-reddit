import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Comment } from '@reddit/core/models/comment.model';
import { User } from '@reddit/core/models/user.model';
import { CommentService } from '@reddit/core/services/comment/comment.service';
import { UserService } from '@reddit/core/services/user/user.service';
import { environment } from '@reddit/env/environment';
import { Router } from '@angular/router';

@Component({
  selector: 'app-comment-group',
  templateUrl: './comment-group.component.html',
  styleUrls: ['./comment-group.component.scss']
})
export class CommentGroupComponent implements OnInit {
  comments: Comment[] = []
  @Input() uuid: string;
  @Input() create_only: boolean = false;
  @Input() user: User;
  @Input() max_nest_depth: number = 0;
  @Input() current_nest_depth: number = 0;
  @Input() parent: number;
  @Input() child_group = false;
  @Input() commentable: boolean = true;

  next = null;
  page = 1;
  is_authenticated: boolean = false;
  comments_count = 0;
  user_checked: boolean = false;
  private loginUrl: string;
  mentioned_users = new Set();
  showLoader: boolean = false;
  @Output() counter = new EventEmitter<number>();
  @Output() create_only_toggle = new EventEmitter<boolean>();
  nested = true;

  constructor(
    private commentService: CommentService,
    private userService: UserService,
    private router: Router
  ) {
    this.loginUrl = `${environment.loginUrl}/`;
  }

  ngOnInit(): void {
    this.showLoader = true;
    if (this.user) {
      this.is_authenticated = true;
    } else {
      this.getUser();
    }
    this.getComments();
  }

  getUser(): void {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if (initialized) {
          this.userService.user.subscribe(
            (user: User) => {
              if (user) {
                this.user = user;
                console.log(this.user);
                this.user_checked = true;
                this.is_authenticated = true;
              } else {
                this.user_checked = true;
                this.is_authenticated = false;
              }
            });
        }
      });
  }

  getComments() {
    this.commentService.getComments(this.uuid, this.page, this.child_group, this.parent).subscribe(
      (response: any) => {
        this.showLoader = false;
        this.setComments(response);
      }, (err) => {
        console.log(err);
        this.showLoader = false;
      }
    );
  }

  loadMoreComments() {
    if (this.next != null) {
      this.getComments();
    }
  }

  setComments(response: any) {
    this.next = response.next;
    if (this.next) {
      this.page = parseInt(this.next.split('=')[1]);
    }
    this.comments = [...this.comments, ...response.results];
    this.comments_count = response.count;
  }

  created(data: any) {
    this.comments.unshift(data);
    this.create_only = false;
    this.counter.emit(this.comments.length);
  }

  goToLogin() {
    // window.location.href = `${this.loginUrl}&continue=${window.location.href}`;
    this.router.navigate(['sign-in']);
  }

  userMentioned(data: any) {
    if (this.mentioned_users.size === 0) {
      this.mentioned_users.add(data);
    } else {
      let user_found = false;
      this.mentioned_users.forEach(
        (user: any) => {
          if (data.id === user.id) {
            user_found = true;
            // this.mentioned_users.add(data);
          }
        });
      if (!user_found) {
        this.mentioned_users.add(data);
      }
    }
    // console.log(this.mentioned_users);
    this.scrollToCreate();
  }

  removeMention(data: any) {
    if (this.mentioned_users.has(data)) {
      this.mentioned_users.delete(data);
    }
  }

  clearComment(data: any) {
    this.mentioned_users.clear();
  }

  scrollToCreate() {
    const el = document.getElementById('createsection');
    el.scrollIntoView({behavior: 'smooth'});
  }
}
