import { Injectable } from '@angular/core';
import { Observable, interval } from 'rxjs';
import { takeWhile } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  displayMessageWordByWord(fullMessage: string, delay: number = 30): Observable<string> {
    return new Observable<string>(observer => {
      let words = fullMessage.split(' ');
      let currentIndex = 0;
      let displayedText = '';

      const timer = interval(delay).pipe(
        takeWhile(() => currentIndex < words.length)
      ).subscribe(() => {
        displayedText += (currentIndex === 0 ? '' : ' ') + words[currentIndex];
        observer.next(displayedText + ' █'); // Add blinking cursor
        currentIndex++;

        if (currentIndex === words.length) {
          observer.next(displayedText); // Remove the cursor at the end
          observer.complete();
        }
      });

      return () => timer.unsubscribe();
    });
  }

  displaySourceWordByWord(source: string, delay: number = 20): Observable<string> {
    return new Observable<string>(observer => {
      let words = source.split(' ');
      let currentIndex = 0;
      let displayedText = '';

      const timer = interval(delay).pipe(
        takeWhile(() => currentIndex < words.length)
      ).subscribe(() => {
        displayedText += (currentIndex === 0 ? '' : ' ') + words[currentIndex];
        observer.next(displayedText + ' █'); // Add blinking cursor
        currentIndex++;

        if (currentIndex === words.length) {
          observer.next(displayedText); // Remove the cursor at the end
          observer.complete();
        }
      });

      return () => timer.unsubscribe();
    });
  }
}
