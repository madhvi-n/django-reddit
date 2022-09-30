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
    this.postService.searchPosts(this.query, this.page).subscribe(
      (response: any) => {
        this.posts = response.results;
      }
    )
  }

}
