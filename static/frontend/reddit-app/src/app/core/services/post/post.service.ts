import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '@reddit/env/environment';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private baseUrl = `${environment.serverUrl}${environment.baseUrl}`;

  constructor(
    public http: HttpClient,
  ) {}

  createPost(postData) {
    return this.http.post(this.baseUrl + 'post/self/', postData);
  }

  getPosts(page:number) {
    return this.http.get(this.baseUrl + 'posts/?page=' + page);
  }

  getPostDetail(uuid: string) {
    return this.http.get(this.baseUrl + 'posts/' + uuid + '/');
  }

  searchPosts(query: string, page: number) {
    return this.http.get(this.baseUrl + 'posts/?search=' + query + '&page=' + page)
  }

  addBookmark(uuid: string, data) {
    return this.http.post(this.baseUrl + 'posts/' + uuid + '/bookmarks/', data);
  }

  removeBookmark(uuid: string, bookmark_id: number) {
    return this.http.delete(this.baseUrl + 'posts/' + uuid + '/bookmarks/' + bookmark_id + '/');
  }

  addVote(uuid: string, data) {
    return this.http.post(this.baseUrl + 'posts/' + uuid + '/votes/', data);
  }

  updateVote(uuid: string, vote_id: number, data) {
    return this.http.put(this.baseUrl + 'posts/' + uuid + '/votes/' + vote_id + '/', data);
  }

  deleteVote(uuid: string, vote_id: number) {
    return this.http.delete(this.baseUrl + 'posts/' + uuid + '/votes/' + vote_id + '/');
  }

}
