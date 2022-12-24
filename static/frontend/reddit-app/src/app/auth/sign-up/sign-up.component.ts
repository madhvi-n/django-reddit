import { AfterViewInit, Component, OnInit, } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { MatSnackBar } from '@angular/material/snack-bar';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent implements OnInit {
  registerForm: FormGroup;
  isLoading: boolean = false;
  hidePassword: boolean = true;
  errors = [];

  constructor(
    private userService: UserService,
    private router: Router,
    private snackbar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.registerForm = new FormGroup({
      first_name: new FormControl('', {
        validators: [Validators.required]
      }),
      last_name: new FormControl('', {
        validators: [Validators.required]
      }),
      email: new FormControl('', {
        validators: [Validators.required, Validators.email]
      }),
      password1: new FormControl('', { validators: [Validators.required] }),
      password2: new FormControl('', { validators: [Validators.required] })
    });
    console.log(this.registerForm);
  }

  get formControl() {
    return this.registerForm.controls;
  }

  toggleVisibility() {
    this.hidePassword = !this.hidePassword;
  }

  onSubmit() {
    const formData = {
      first_name: this.registerForm.value.first_name,
      last_name: this.registerForm.value.last_name,
      email: this.registerForm.value.email,
      password1: this.registerForm.value.password1,
      password2: this.registerForm.value.password2
    };
    this.isLoading = true;
    this.userService.register(formData).subscribe(
      (result) => {
        this.isLoading = false;
        this.registerForm.reset();
        this.snackbar.open('Registered successfully. Proceed to login');
        this.router.navigate(['sign-in']);
      },
      (err) => {
        this.isLoading = false;
        if(err.error.password1){
          this.snackbar.open(`${err.error.password1[0]}`);
        }
        if(err.error.email){
          this.snackbar.open(`${err.error.email[0]}`);
        }
      }
    );
  }
}
