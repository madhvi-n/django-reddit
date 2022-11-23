import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { PostService } from '@reddit/core/services/post/post.service';
import { Post } from '@reddit/core/models/post.model';
import { User } from '@reddit/core/models/user.model';


@Component({
  selector: 'app-post-detail',
  templateUrl: './post-detail.component.html',
  styleUrls: ['./post-detail.component.scss']
})
export class PostDetailComponent implements OnInit {
  post: Post;
  user: User;
  post_uuid: string;
  isLoading: boolean = true;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private postService: PostService
  ) { }

  ngOnInit(): void {
    this.post_uuid = this.route.snapshot.params.uuid;
    this.getAuthUser();
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
    this.getPostDetail();
  }

  getPostDetail() {
    this.postService.getPostDetail(this.post_uuid).subscribe(
      (response: any) => {
        this.post = response;
        this.isLoading = false;
      })
  }
}
