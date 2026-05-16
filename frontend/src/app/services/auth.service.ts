import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';

export interface User {
  _id: string;
  username: string;
  email: string;
  level: number;
  country: string;
  token?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;

  constructor(private http: HttpClient, private router: Router) {
    const savedUser = localStorage.getItem('currentUser');
    this.currentUserSubject = new BehaviorSubject<User | null>(
      savedUser ? JSON.parse(savedUser) : null
    );
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  get isGuest(): boolean {
    return localStorage.getItem('isGuest') === 'true';
  }

  login(credentials: any): Observable<User> {
    return this.http.post<User>('/api/auth/login', credentials).pipe(
      tap(user => {
        if (user && user.token) {
          this.clearGuestMode();
          localStorage.setItem('currentUser', JSON.stringify(user));
          this.currentUserSubject.next(user);
        }
      })
    );
  }

  register(userData: any): Observable<User> {
    // Add default values for required fields in the backend
    const data = {
      level: 1,
      country: 'US',
      ...userData
    };
    return this.http.post<User>('/api/auth/register', data).pipe(
      tap(user => {
        if (user && user.token) {
          this.clearGuestMode();
          localStorage.setItem('currentUser', JSON.stringify(user));
          this.currentUserSubject.next(user);
        }
      })
    );
  }

  setGuestMode() {
    this.logout();
    localStorage.setItem('isGuest', 'true');
  }

  clearGuestMode() {
    localStorage.removeItem('isGuest');
  }

  logout() {
    localStorage.removeItem('currentUser');
    this.clearGuestMode();
    this.currentUserSubject.next(null);
    this.router.navigate(['/authentication/login']);
  }

  getToken(): string | null {
    const user = this.currentUserValue;
    return user ? user.token || null : null;
  }

  isLoggedIn(): boolean {
    return !!this.currentUserValue;
  }
}
