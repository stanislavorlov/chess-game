import { Component } from '@angular/core';
import { CoreService } from 'src/app/services/core.service';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MaterialModule } from 'src/app/material.module';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-side-register',
  standalone: true,
  imports: [RouterModule, MaterialModule, FormsModule, ReactiveFormsModule, CommonModule],
  templateUrl: './side-register.component.html',
})
export class AppSideRegisterComponent {
  errorMessage: string = '';

  constructor(private settings: CoreService, private authService: AuthService, private router: Router) { }

  form = new FormGroup({
    username: new FormControl('', [Validators.required, Validators.minLength(6)]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)]),
  });

  get f() {
    return this.form.controls;
  }

  submit() {
    if (this.form.invalid) {
      return;
    }

    this.authService.register(this.form.value).subscribe({
      next: () => {
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Registration failed. Please try again.';
      }
    });
  }

  playAsGuest() {
    this.authService.setGuestMode();
    this.router.navigate(['/']);
  }
}
