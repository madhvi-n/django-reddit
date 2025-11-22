import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '@reddit/env/environment';

@Injectable({
  providedIn: 'root'
})
export class GroupService {
  private baseUrl = `${environment.serverUrl}${environment.baseUrl}`;

  constructor(
    public http: HttpClient,
  ) {}

  createGroup(postData){
    return this.http.post(this.baseUrl + 'groups/', postData);
  }

  getGroups() {
    return this.http.get(this.baseUrl + 'groups/');
  }

  getGroupPosts(group_id: number){
    return this.http.get(this.baseUrl + 'groups/' + group_id + '/posts/');
  }

  getGroupDetail(group_id: number) {
    return this.http.get(this.baseUrl + 'groups/' + group_id + '/');
  }

  getUserGroups(group_type: string, user_id: number, member_type: string){
    return this.http.get(
      this.baseUrl + 'groups/?group_type=' + group_type + '&members__user=' + user_id
        + '&members__member_type=' + member_type
    );
  }

  filterMembers(member_type: string, group_id: number | string, user:number | string){
    return this.http.get(
      this.baseUrl + 'members/?member_type=' + member_type + '&group=' + group_id + '&user=' + user
    );
  }

  joinGroup(group_id: number, data) {
    return this.http.post(this.baseUrl + 'groups/' + group_id + '/member_requests/', data)
  }

  cancelRequest(group_id: number, request_id: number) {
    return this.http.delete(this.baseUrl + 'groups/' + group_id + '/member_requests/' + request_id + '/');
  }

  leaveGroup(group_id: number, data) {
    return this.http.put(this.baseUrl + 'groups/' + group_id + '/leave_group/', data);
  }

  inviteMember(group_id: number, data) {
    return this.http.post(this.baseUrl + 'groups/' + group_id + '/invites/', data)
  }

  addGroupRule(group_id: number, data) {
    return this.http.post(this.baseUrl + 'groups/' + group_id + '/rules/', data)
  }


}
