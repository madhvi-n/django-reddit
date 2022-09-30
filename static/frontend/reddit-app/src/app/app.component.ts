import { AfterContentChecked, Component, OnInit } from '@angular/core';
import { UserService } from './core/services/user/user.service';
import { StorageHandlerService } from './core/services/storage/storage-handler.service';
import { CookieService } from 'ngx-cookie-service';
import { User } from './core/models/user.model';
import { environment } from '@reddit/env/environment';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';
import { debounceTime, distinctUntilChanged } from "rxjs/operators";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterContentChecked {
  title = 'reddit';
  path: string;
  authRoute: boolean = false;
  user: User;
  value = 'Search';
  searchField: FormGroup;

  constructor(
    private router: Router,
    private userService: UserService,
    private cookieService: CookieService,
    private storage: StorageHandlerService
  ) {
    this.router.events.subscribe(
      () => this.path = this.router.url
    );
    this.path = this.router.url;
  }

  ngOnInit(): void {
    this.searchField = new FormGroup({
      search: new FormControl('')
    });
    this.userService.fetchUser((user) => this.user = user);
  }

  ngAfterContentChecked(): void {
    if (this.path.includes('/sign-in')
      || this.path.includes('/sign-up')
      || this.path.includes('logout')) {
        this.authRoute = true;
    } else {
      this.authRoute = false;
    }
  }

  logout() {
    this.userService.logout().subscribe(
      (response) => {
        this.storage.removeItem('user');
        window.location.href = `${environment.loginUrl}`;
      },
      (error) => {
        console.log(error);
      });
  }

  search() {

    this.router.navigate(['search'], {
      queryParams: {
        query: this.searchField.value.search,
      },
    });
    this.searchField.reset();
  }
}
