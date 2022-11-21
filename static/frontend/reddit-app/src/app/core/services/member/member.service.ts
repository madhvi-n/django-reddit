import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '@reddit/env/environment';

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  private baseUrl = `${environment.serverUrl}${environment.baseUrl}`;

  constructor(
    public http: HttpClient,
  ) {}

  joinGroup(){

  }

  inviteMember(){

  }

}
