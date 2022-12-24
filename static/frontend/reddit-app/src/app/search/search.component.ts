import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { PostService } from '@reddit/core/services/post/post.service';
import { User } from '@reddit/core/models/user.model';
import { Post } from '@reddit/core/models/post.model';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  posts: Post[] = []
  query: string = '';
  page: number = 1;
  isLoading: boolean = false;
  showLoader: boolean = false;
  next: string;

  constructor(
    private postService: PostService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(
      (params) => {
        this.query = params.query;
      })
    this.fetchPosts();
  }

  fetchPosts() {
    this.postService.filterPosts(this.page, this.query, '', '', '').subscribe(
      (response: any) => {
        this.posts = [...this.posts, ...response.results];
        this.next = response.next;
        if (this.next) {
          const page_params = this.next.split('&')[2];
          this.page = parseInt(page_params.split('=')[1]);
          console.log(this.page);
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
    this.fetchPosts();
  }
}
