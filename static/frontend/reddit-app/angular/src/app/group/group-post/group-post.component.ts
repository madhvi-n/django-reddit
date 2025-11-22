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
  selector: 'app-group-post',
  templateUrl: './group-post.component.html',
  styleUrls: ['./group-post.component.scss']
})
export class GroupPostComponent implements OnInit {
  group: Group;
  user: User;

  constructor(
    private groupService: GroupService,
    private userService: UserService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    const group_id = this.route.snapshot.params.id;
    if(group_id){
      this.getGroupDetail(group_id);
    }
    this.getAuthUser();
  }

  getAuthUser(): void {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if (initialized) {
          this.userService.user.subscribe(
            (user: User) => {
              this.user = user;
              console.log(this.user);
            });
        }
      });
  }

  getGroupDetail(group_id: number){
    this.groupService.getGroupDetail(group_id).subscribe(
      (response: Group) => {
        this.group = response;
      },
      (err: any) => {
        console.log(err);
      })
  }

}
