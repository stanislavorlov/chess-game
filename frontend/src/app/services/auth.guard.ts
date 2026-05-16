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

    // List of routes that REQUIRE a real account
    const restrictedRoutes = ['/stats', '/profile'];
    const isRestricted = restrictedRoutes.some(path => state.url.startsWith(path));

    if (isRestricted) {
        if (isLoggedIn) {
            return true;
        }
        this.router.navigate(['/authentication/login']);
        return false;
    }

    // For all other routes, allow access. 
    // If not logged in and not guest, automatically set guest mode.
    if (!isLoggedIn && !isGuest) {
        this.authService.setGuestMode();
    }
    
    return true;
  }
}
