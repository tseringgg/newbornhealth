// theme.service.ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private isDarkTheme = false;

  constructor() {
    // Load theme from localStorage on initialization
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme === 'dark') {
      this.enableDarkTheme();
    } else {
      this.enableLightTheme();
    }
  }

  enableDarkTheme(): void {
    document.body.classList.add('dark-theme');
    this.isDarkTheme = true;
    localStorage.setItem('theme', 'dark');
  }

  enableLightTheme(): void {
    document.body.classList.remove('dark-theme');
    this.isDarkTheme = false;
    localStorage.setItem('theme', 'light');
  }

  toggleTheme(): void {
    if (this.isDarkTheme) {
      this.enableLightTheme();
    } else {
      this.enableDarkTheme();
    }
  }

  get isDarkMode(): boolean {
    return this.isDarkTheme;
  }
}