import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { PostService } from '@reddit/core/services/post/post.service';
import { UserService } from '@reddit/core/services/user/user.service';
import { GroupService } from '@reddit/core/services/group/group.service';
import { User } from '@reddit/core/models/user.model';
import { Post } from '@reddit/core/models/post.model';
import { Group } from '@reddit/core/models/group.model';

@Component({
  selector: 'app-group-feed',
  templateUrl: './group-feed.component.html',
  styleUrls: ['./group-feed.component.scss']
})
export class GroupFeedComponent implements OnInit {
  groupPosts: Post[] = []
  user: User;
  @Input() group: Group;
  isLoading: boolean = true;

  constructor(
    private groupService: GroupService,
    private userService: UserService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.getAuthUser();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if(this.group){
      this.getFeed();
    }
  }

  getAuthUser(): void {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if (initialized) {
          this.userService.user.subscribe(
            (user: User) => {
              this.user = user;
            });
        }
      });
  }

  getFeed(){
    this.groupService.getGroupPosts(this.group.id).subscribe(
      (response: any) => {
        this.groupPosts = response;
        console.log(this.groupPosts);
        this.isLoading = false;
      },
      (err: any) => {
        console.log(err);
        this.isLoading = false;
      })
  }

  redirect(){
    this.router.navigate(['submit-post'], {relativeTo: this.route})
  }

}
