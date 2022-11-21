import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '@reddit/env/environment';
import { User } from '@reddit/core/models/user.model';
import { StorageHandlerService } from '../storage/storage-handler.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private serverUrl = `${environment.serverUrl}`;
  user: BehaviorSubject<User>;
  userInitialized = new BehaviorSubject(false);

  constructor(
    public http: HttpClient,
    private storage: StorageHandlerService
  ) {}

  setUser(user: User, callback?: (user: User) => any): void {
    this.user = new BehaviorSubject(user);
    if (user) {
      this.storage.storeItem('user', user);
    }
    this.userInitialized.next(true);
    if (callback) {
      callback(user);
    }
  }

  unsetUser(): void {
    this.user.next(null);
    this.storage.removeItem('user');
  }

  fetchUser(callback: (user: User) => any): void {
    if (this.user?.value) {
      callback(this.user.value);
    }
    const storageUser = this.storage.getItem('user');
    if (storageUser) {
      this.setUser(storageUser, callback);
    } else {
      this.getAuthUser((user) => this.setUser(user, callback));
    }
  }

  getAuthUser(callback: (user: User) => any): void {
    this.http.get(this.serverUrl + '/api/v1/users/auth/').subscribe(
      (response: Object) => {
        callback(response as User);
      }, (error: any) => {
        callback(null);
      }
    );
  }

  register(postData) {
    return this.http.post(this.serverUrl + '/rest-auth/registration/', postData);
  }

  login(postData) {
    return this.http.post(this.serverUrl + '/rest-auth/login/', postData);
  }

  logout() {
    return this.http.post(this.serverUrl + '/rest-auth/logout/', {});
  }

  addInterests(username: string) {
    return;
  }
}
