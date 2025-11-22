import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { GroupService } from '@reddit/core/services/group/group.service';
import { Group } from '@reddit/core/models/group.model';
import { User } from '@reddit/core/models/user.model';
import { MatDialog } from '@angular/material/dialog';
import { ConfirmationDialogComponent } from '@reddit/app/components/confirmation-dialog/confirmation-dialog.component';

@Component({
  selector: 'app-group',
  templateUrl: './group.component.html',
  styleUrls: ['./group.component.scss']
})
export class GroupComponent implements OnInit {
  group: Group;
  user: User;
  group_id: number;
  moderators = [];

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private groupService: GroupService,
    private dialog: MatDialog
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
              // console.log(this.user);
            });
        }
      });
  }

  getGroupDetail(group_id: number){
    this.groupService.getGroupDetail(group_id).subscribe(
      (response: Group) => {
        console.log(response);
        this.group = response;
        this.getModerators();
      },
      (err: any) => {
        console.log(err);
      })
  }

  getModerators(){
    this.groupService.filterMembers('MODERATOR', this.group.id, '').subscribe(
      (response: any) => {
        this.moderators = response.results;
      })
  }

  joinGroup() {
    if(!this.user) return;
    const data = {
      group: this.group.id,
      user: this.user.id
    }
    this.groupService.joinGroup(this.group.id, data).subscribe(
      (response: any) => {
        this.group.member_status = response;
      }
    )
  }

  cancel() {
    if(!this.user) return;
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: {
        message: `Are you sure you want to leave the g/${this.group.name} group?`,
      },
      height: '205px',
      width: '410px'
    })
    dialogRef.afterClosed().subscribe(
      (response) => {
        console.log(response);
        if(response) {
          const data = {
            user: this.user.id,
            member_request: this.group.member_status.id
          }
          this.groupService.cancelRequest(this.group.id, this.group.member_status.id).subscribe(
            (response: any) => {
              if(response.success) {
                this.group.member_status = null;
              }
            })
        }
      })

  }

  leaveGroup() {
    if(!this.user) return;
    // open confirmation dialog
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      data: {
        message: `Are you sure you want to leave the g/${this.group.name} group?`,
      },
      height: '205px',
      width: '410px'
    })
    // call leave group api
    dialogRef.afterClosed().subscribe(
      (response) => {
        console.log(response);
        if(response) {
          const data = {
            user: this.user.id,
            member_request: this.group.member_status.id
          }
          this.groupService.leaveGroup(this.group.id, data).subscribe(
            (response: any) => {
              this.group.member_status = null;
            })
        }
      })
  }
}
