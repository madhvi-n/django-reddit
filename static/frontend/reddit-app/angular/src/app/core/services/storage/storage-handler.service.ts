import { Injectable } from '@angular/core';
import { environment } from '@reddit/env/environment';
import { HttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';
import { User } from '@reddit/core/models/user.model';

@Injectable({
  providedIn: 'root'
})
export class StorageHandlerService {
  private baseUrl: string = `${environment.baseUrl}`;
  authChange: Subject<User> = new Subject();
  user: User;
  authenticated: boolean = false;

  constructor(private http: HttpClient) {
    this.baseUrl = `${environment.serverUrl}${this.baseUrl}`;
  }

  storeItem(key: string, value: any): void {
    let stringifiedValue = JSON.stringify(value);
    stringifiedValue = stringifiedValue.replace(/\s/g, '');
    const encodedValue = btoa(unescape(stringifiedValue));
    localStorage.setItem(key, encodedValue);
  }

  getItem(key: string): any {
    const data = localStorage.getItem(key);
    if (data !== null) {
      const decodedString = decodeURIComponent(escape(atob(data)));
      const jsonData = JSON.parse(decodedString);
      return jsonData;
    }
    return null;
  }

  removeItem(key: string): void {
    localStorage.removeItem(key);
  }

  getUser() {
    return this.http.get(this.baseUrl + 'users/auth/');
  }

  getCurrentUserSubject() {
    return this.user;
  }

  getCurrentUserLocalStorage() {
    var data = localStorage.getItem('user');
    if(data) {
      const decodedString = decodeURIComponent(escape(atob(data)));
      var jsonData = JSON.parse(decodedString);
      return jsonData;
    }
    else {
      return data;
    }
  }

  setCurrentUserLocalStorage(user) {
    let stringifyData = JSON.stringify(user);
    stringifyData = stringifyData.replace(/\s/g, '');
    const encodedUrl = btoa(unescape(stringifyData));
    if(this.getCurrentUserLocalStorage() != null) {
      localStorage.removeItem('user');
    }
    localStorage.setItem('user', encodedUrl);
  }

}
