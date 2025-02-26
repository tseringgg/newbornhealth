import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  // private apiUrl = 'http://127.0.0.1:5000/ask';
  // private apiUrl = 'https://newbornhealthapi-h3ftfxe4ewfrargp.centralus-01.azurewebsites.net/ask';
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  askQuestion(question: string): Observable<any> {
    let x = this.http.post<any>(this.apiUrl, { question });
    return x;
  }
}
