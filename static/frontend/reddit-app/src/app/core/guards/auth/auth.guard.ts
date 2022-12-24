import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';

import { environment } from '@reddit/env/environment';
import { UserService } from '@reddit/core/services/user/user.service';
import { User } from '@reddit/core/models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  private serverUrl: string;
  private user: User;
  authenticated: boolean = false;

  constructor(
    private userService: UserService,
  ) {
    this.serverUrl = `${environment.serverUrl}`;
  }

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    this.userService.fetchUser((user) => {
      this.user = user;
    });
    if (this.user || this.userService.user?.getValue()) {
      return true;
    }
    return false;
  }

}
