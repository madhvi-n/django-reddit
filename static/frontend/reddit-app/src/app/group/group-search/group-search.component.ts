import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { GroupService } from '@reddit/core/services/group/group.service';
import { Group } from '@reddit/core/models/group.model';
import { User } from '@reddit/core/models/user.model';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '@reddit/app/components/confirmation-dialog/confirmation-dialog.component';

@Component({
  selector: 'app-group-search',
  templateUrl: './group-search.component.html',
  styleUrls: ['./group-search.component.scss']
})
export class GroupSearchComponent implements OnInit {
  groups = [];
  user: User;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private groupService: GroupService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.getGroups();
    this.getAuthUser();
  }

  getGroups(){
    this.groupService.getGroups().subscribe(
      (response: any) => {
        this.groups = response;
      })
  }

  getAuthUser(): void {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if (initialized) {
          this.userService.user.subscribe(
            (user: User) => {
              this.user = user;
              // console.log(this.user);
            });
        }
      });
  }

  joinGroup(group_id: number) {
    this.router.navigate(['groups', group_id]);
  }

  cancel(group_id: number) {
    this.router.navigate(['groups', group_id]);
  }

  leaveGroup(group_id: number) {
    this.router.navigate(['groups', group_id]);
  }
}
