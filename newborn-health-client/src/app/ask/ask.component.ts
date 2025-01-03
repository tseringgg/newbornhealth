import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-ask',
  standalone: false,
  //imports: [FormsModule, CommonModule, HttpClientModule],
  templateUrl: './ask.component.html',
  styleUrl: './ask.component.scss'
})
export class AskComponent {
  question: string = '';
  response: string = '';

  constructor(private dataService: DataService) { }

  ask() {
    if (this.question.trim()) {
      this.dataService.askQuestion(this.question).subscribe(
        data => this.response = data.response,
        error => console.error('Error:', error)
      );
    }
  }
}
