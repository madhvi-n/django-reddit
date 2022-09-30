import { Component, OnInit } from '@angular/core';
import { UserService } from '../core/services/user/user.service';
import { PostService } from '../core/services/post/post.service';
import { User } from '../core/models/user.model';
import { Post } from '../core/models/post.model';

@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  styleUrls: ['./feed.component.scss']
})

export class FeedComponent implements OnInit {
  isLoading: boolean = false;
  user: User;
  posts: Post[] = [];
  page: number = 1;
  showLoader: boolean = false;
  next: string;

  constructor(
    private userService: UserService,
    private postService: PostService
  ) { }

  ngOnInit(): void {
    this.getAuthUser();
    this.getPosts();
  }

  getAuthUser() {
    this.userService.userInitialized.subscribe(
      (initialized: boolean) => {
        if(initialized) {
          this.userService.user.subscribe(
            (response: User) => {
              this.user = response;
            })
        }
      })
  }

  getPosts() {
    if (!this.showLoader) {
      this.isLoading = true;
    }
    console.log(this.page)
    this.postService.getPosts(this.page).subscribe(
      (response: any) => {
        this.posts = [...this.posts, ...response.results];
        this.next = response.next;
        if (this.next) {
          this.page = parseInt(this.next.split('=')[1]);
        }
        this.isLoading = false;
        this.showLoader = false;
      },
      (err) => {
        console.log(err);
        this.isLoading = false;
        this.showLoader = false;
    });
  }

  // vote(post) {
  //   if(post.author.id === this.user.id) {
  //     return;
  //   }
  //
  //   const data = {
  //     user: this.user.id,
  //     post: post
  //   }
  //
  //   this.postService.addVote(post, data).subscribe(
  //     (response) => {
  //       console.log(response);
  //     },
  //     (err) => {
  //       console.log(err);
  //     })
  // }
  //
  // removeVote(uuid, vote_id) {
  //   this.postService.deleteVote(uuid, vote_id).subscribe(
  //     (response: any) => {
  //       console.log('vote removed')
  //     });
  // }

  loadMorePosts(): void {
    this.showLoader = true;
    this.getPosts();
  }
}
