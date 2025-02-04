import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PdfViewerService {
  constructor(private http: HttpClient) {}

  getPdfFiles(): Observable<string[]> {
    let response = this.http.get<string[]>('http://localhost:4200/assets/pdfs.json');
    console.log('response was received');
    return response;
  }

// Replaced this method with a python script
//   updatePdfList(): Observable<string[]> {
//     return this.http.get<string[]>(`${environment.apiUrl}/pdfs`).pipe(
//       tap((pdfFiles: string[]) => {
//         this.http.post<void>('http://localhost:4200/assets/pdfs.json', pdfFiles).subscribe();
//       })
//     );
//   }
}
