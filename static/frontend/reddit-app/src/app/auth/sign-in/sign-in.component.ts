import { AfterViewInit, Component, OnInit, } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../../core/services/user/user.service';


@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss']
})
export class SignInComponent implements OnInit {
  loginForm: FormGroup;
  isLoading: boolean = false;
  hidePassword: boolean = true;

  constructor(
    private userService: UserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      email: new FormControl('', {
        validators: [Validators.required, Validators.email]
      }),
      password: new FormControl('', { validators: [Validators.required] })
    });
  }

  toggleVisibility() {
    this.hidePassword = !this.hidePassword;
  }

  onSubmit() {
    const loginData = {
      email: this.loginForm.value.email,
      password: this.loginForm.value.password
    };
    console.log(loginData);
    this.isLoading = true;
    this.userService.login(loginData).subscribe(
      (result) => {
        this.isLoading = false;
        this.router.navigate([''])
        // if (this.route.snapshot.queryParams.continue) {
        //   window.location.href = this.route.snapshot.queryParams.continue;
        // } else {
        //   this.router.navigate(['']);
        // }
      },
      (err) => {
        this.isLoading = false;
        // console.log(err.error);
        // this.errors = err.error.non_field_errors;
        // if (this.errors.includes('E-mail is not verified.')) {
        //   this.authService.resendVerificationEmail(this.loginForm.value.email).subscribe(
        //     () => {
        //       this.snackbarService.error('Verification email sent');
        //     }
        //   );
        // }
        // this.snackbarService.error(this.errors[0]);
      }
    );
  }

}
