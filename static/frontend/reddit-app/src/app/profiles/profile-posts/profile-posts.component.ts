import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { PostService } from '@reddit/core/services/post/post.service';
import { User } from '@reddit/core/models/user.model';
import { Post } from '@reddit/core/models/post.model';

@Component({
  selector: 'app-profile-posts',
  templateUrl: './profile-posts.component.html',
  styleUrls: ['./profile-posts.component.scss']
})
export class ProfilePostsComponent implements OnInit {
  @Input() user: User;
  @Input() self: boolean;
  @Input() currentUser: string;

  posts: Post[] = [];
  page: number = 1;
  isLoading: boolean = false;
  showLoader: boolean = false;
  next: string;
  
  constructor(
    private userService: UserService,
    private postService: PostService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.getPosts();
  }

  getPosts(){
    this.postService.filterPosts(this.page, '', '', '', this.currentUser).subscribe(
      (response: any) => {
        this.posts = [...this.posts, ...response.results];
        this.next = response.next;
        if (this.next) {
          this.page = parseInt(this.next.split('=')[1]);
        }
        this.isLoading = false;
        this.showLoader = false;
      },
      (err: any) => {
        console.log(err);
        this.isLoading = false;
        this.showLoader = false;
      })
  }

  loadMorePosts(): void {
    this.showLoader = true;
    this.getPosts();
  }

}
