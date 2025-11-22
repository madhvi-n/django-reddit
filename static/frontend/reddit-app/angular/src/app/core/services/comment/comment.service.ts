import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@reddit/env/environment';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private baseUrl = `${environment.serverUrl}${environment.baseUrl}`;

  constructor(public http: HttpClient) {}

  getComments(uuid: string, page: number = 1, children = false, parent = 0) {
    if (children) {
      return this.http.get(this.baseUrl + 'posts/' + uuid + '/comments/' + parent + '/children/?page=' + page);
    } else {
      return this.http.get(this.baseUrl + 'posts/' + uuid + '/comments/?page=' + page);
    }
  }

  createComment(uuid: string, comment) {
    return this.http.post(this.baseUrl + 'posts/' + uuid + '/comments/', comment);
  }

  updateComment(uuid: string, comment_pk: number, comment) {
    return this.http.put(this.baseUrl + 'posts/' + uuid + '/comments/' + comment_pk + '/', comment);
  }

  removeComment(uuid: string, comment_pk: number) {
    return this.http.delete(this.baseUrl + 'posts/' + uuid + '/comments/' + comment_pk + '/');
  }

  checkUserVote(uuid: string, comment_pk: number) {
    return this.http.get(this.baseUrl + 'posts/' + uuid + '/comments/' + comment_pk + '/check_vote/');
  }

  upvoteComment(uuid: string, comment_pk: number) {
    return this.http.put(this.baseUrl + 'posts/' + uuid + '/comments/' + comment_pk + '/upvote/', {});
  }

  downvoteComment(uuid: string, comment_pk: number) {
    return this.http.put(this.baseUrl + 'posts/' + uuid + '/comments/' + comment_pk + '/downvote/', {});
  }

  removeVote(uuid: string, comment_pk: number) {
    return this.http.delete(this.baseUrl + 'posts/' + uuid + '/comments/' + comment_pk + '/remove_vote/', {});
  }

  userComments(username: string){
    return this.http.get(this.baseUrl + 'users/' + username + '/user_comments/');
  }

}
