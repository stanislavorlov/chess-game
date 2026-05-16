import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    const isLoggedIn = this.authService.isLoggedIn();
    const isGuest = this.authService.isGuest;

    // dashboard and play are accessible to everyone
    if (state.url.startsWith('/dashboard') || state.url.startsWith('/play')) {
        return true;
    }

    // Stats and Profile require real login
    if (isLoggedIn) {
      return true;
    }

    // If not logged in (even if guest), redirect to login for protected routes
    this.router.navigate(['/authentication/login']);
    return false;
  }
}
