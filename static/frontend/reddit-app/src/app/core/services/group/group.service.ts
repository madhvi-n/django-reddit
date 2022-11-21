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
    return this.http.post(this.baseUrl + 'group/self/', postData);
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

  filterMembers(member_type: string, user:number){
    return this.http.get(
      this.baseUrl + 'members/?member_type=' + member_type + '&user=' + user
    );
  }
}
