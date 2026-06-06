import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import { MaterialModule } from 'src/app/material.module';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-side-login',
  standalone: true,
  imports: [RouterModule, MaterialModule, FormsModule, ReactiveFormsModule, CommonModule],
  templateUrl: './side-login.component.html',
})
export class AppSideLoginComponent {
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) { }

  form = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required]),
  });

  get f() {
    return this.form.controls;
  }

  submit() {
    if (this.form.invalid) {
      return;
    }

    const credentials = {
      email: this.form.value.email,
      password: this.form.value.password
    };

    this.authService.login(credentials).subscribe({
      next: () => {
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Invalid email or password';
      }
    });
  }

  playAsGuest() {
    this.authService.setGuestMode();
    this.router.navigate(['/']);
  }
}
