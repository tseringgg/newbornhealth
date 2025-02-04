import { Component, OnInit } from '@angular/core';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { NgxExtendedPdfViewerModule } from 'ngx-extended-pdf-viewer';
import { PdfViewerService } from './pdf-viewer.service';
//import { ExamplePdfViewerComponent } from './example-pdf-viewer/example-pdf-viewer.component';

@Component({
  selector: 'app-pdf-viewer',
  standalone: true,
  imports: [MatMenuModule, MatButtonModule, NgxExtendedPdfViewerModule, CommonModule],
  templateUrl: './pdf-viewer.component.html',
  styleUrl: './pdf-viewer.component.scss'
})
export class PdfViewerComponent implements OnInit {
  pdfFiles: string[] = [];
  selectedPdf: string = '/assets/pdfs/GLUCOSE GEL (1).pdf';

  constructor(private pdfViewerService: PdfViewerService) {}

  ngOnInit() {
    this.loadPdfFiles();
  }

  loadPdfFiles() {
    this.pdfViewerService.getPdfFiles().subscribe(
      files => {
        this.pdfFiles = files;
        alert("PDFs loaded");
      },
      error => {
        console.error('Error loading PDF files:', error);
        alert('Failed to load PDF files');
      }
    );
  }

  selectPdf(pdf: string) {
    this.selectedPdf = `http://localhost:4200/assets/pdfs/${pdf}`;
  }
}
