import { Component, ChangeDetectionStrategy, ChangeDetectorRef, DestroyRef, inject, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';
import { MaterialModule } from 'src/app/material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [RouterModule, MaterialModule, FormsModule, ReactiveFormsModule, CommonModule],
  templateUrl: './reset-password.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ResetPasswordComponent implements OnInit {
  errorMessage: string = '';
  successMessage: string = '';
  token: string = '';

  private readonly destroyRef = inject(DestroyRef);
  private readonly cdr = inject(ChangeDetectorRef);

  constructor(
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  form = new FormGroup({
    password: new FormControl('', [Validators.required]),
    confirmPassword: new FormControl('', [Validators.required]),
  }, { validators: this.passwordMatchValidator });

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password')?.value;
    const confirmPassword = control.get('confirmPassword')?.value;

    if (password || confirmPassword) {
      if (password !== confirmPassword) {
        control.get('confirmPassword')?.setErrors({ passwordMismatch: true });
        return { passwordMismatch: true };
      } else {
        const confirmErrors = control.get('confirmPassword')?.errors;
        if (confirmErrors) {
          delete confirmErrors['passwordMismatch'];
          if (Object.keys(confirmErrors).length === 0) {
            control.get('confirmPassword')?.setErrors(null);
          } else {
            control.get('confirmPassword')?.setErrors(confirmErrors);
          }
        }
      }
    }
    return null;
  }

  get f() {
    return this.form.controls;
  }

  ngOnInit() {
    this.token = this.route.snapshot.paramMap.get('token') || '';
    if (!this.token) {
      this.errorMessage = 'Invalid password reset token.';
    }
  }

  submit() {
    if (this.form.invalid || !this.token) {
      return;
    }

    this.errorMessage = '';
    this.successMessage = '';

    const password = this.form.value.password;
    if (password) {
      this.authService.resetPassword(this.token, password)
        .pipe(takeUntilDestroyed(this.destroyRef))
        .subscribe({
          next: () => {
            this.successMessage = 'Password updated successfully. Redirecting to login...';
            this.cdr.markForCheck();
            setTimeout(() => {
              this.router.navigate(['/authentication/login']);
            }, 3000);
          },
          error: (err) => {
            this.errorMessage = err.error?.message || 'Failed to reset password';
            this.cdr.markForCheck();
          }
        });
    }
  }
}
