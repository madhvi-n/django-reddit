import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { GroupService } from '@reddit/core/services/group/group.service';
import { Group } from '@reddit/core/models/group.model';
import { User } from '@reddit/core/models/user.model';

@Component({
  selector: 'app-group',
  templateUrl: './group.component.html',
  styleUrls: ['./group.component.scss']
})
export class GroupComponent implements OnInit {
  group: Group;
  user: User;
  group_id: number;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private groupService: GroupService
  ) { }

  ngOnInit(): void {
    this.group_id = this.route.snapshot.params.id;
    this.getAuthUser();
    this.getGroupDetail(this.group_id);
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
        console.log(response);
        this.group = response;
      },
      (err: any) => {
        console.log(err);
      })
  }
}
