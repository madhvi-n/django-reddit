import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { User } from '@reddit/core/models/user.model';
import { Group } from '@reddit/core/models/group.model';

@Component({
  selector: 'app-profile-bookmarks',
  templateUrl: './profile-bookmarks.component.html',
  styleUrls: ['./profile-bookmarks.component.scss']
})
export class ProfileBookmarksComponent implements OnInit {
  isLoading: boolean = false;
  @Input() user: User;
  bookmarks = [];

  constructor(
    private userService: UserService,
    private route: ActivatedRoute,
    private router: Router
  ) { }


  ngOnInit(): void {
    this.getUserBookmarks();
  }

  getUserBookmarks(){
    this.userService.getBookmarks(this.user.username).subscribe(
      (response: any) => {
        this.bookmarks = response;
      })
  }

}
