import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, DestroyRef, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { AuthService, UpdateProfileData } from '../../../services/auth.service';
import { CommonModule } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProfileComponent implements OnInit {
  profileForm: FormGroup;
  isLoading = false;

  private readonly destroyRef = inject(DestroyRef);
  private readonly cdr = inject(ChangeDetectorRef);

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) {
    this.profileForm = this.fb.group({
      firstName: [''],
      lastName: [''],
      country: [''],
      password: ['']
    });
  }

  ngOnInit(): void {
    const user = this.authService.currentUserValue;
    if (user) {
      this.profileForm.patchValue({
        firstName: user.firstName || '',
        lastName: user.lastName || '',
        country: user.country || ''
      });
      this.cdr.markForCheck();
    }
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      this.isLoading = true;
      this.cdr.markForCheck();
      const formValue = this.profileForm.value;
      
      // If password is empty, don't send it to avoid overwriting with empty
      const payload: UpdateProfileData = {
        firstName: formValue.firstName || '',
        lastName: formValue.lastName || '',
        country: formValue.country || ''
      };
      if (formValue.password) {
        payload.password = formValue.password;
      }

      this.authService.updateProfile(payload)
        .pipe(takeUntilDestroyed(this.destroyRef))
        .subscribe({
          next: (updatedUser) => {
            this.isLoading = false;
            this.profileForm.patchValue({ password: '' }); // Clear password field
            this.snackBar.open('Profile updated successfully!', 'Close', { duration: 3000 });
            this.cdr.markForCheck();
          },
          error: (err) => {
            this.isLoading = false;
            this.snackBar.open('Failed to update profile', 'Close', { duration: 3000 });
            console.error(err);
            this.cdr.markForCheck();
          }
        });
    }
  }
}
