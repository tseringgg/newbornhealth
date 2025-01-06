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
  questions: { question: string, response: string }[] = [];
  newQuestion: string = '';

  constructor(private dataService: DataService) { }

  ask(q: { question: string, response: string }) {
    if (q.question.trim()) {
      this.dataService.askQuestion(q.question).subscribe(
        data => q.response = data.response,
        error => console.error('Error:', error)
      );
    }
  }

  addQuestion() {
    if (this.newQuestion.trim()) {
      const newQ = { question: this.newQuestion, response: '' };
      this.questions.push(newQ);
      this.ask(newQ);
      this.newQuestion = '';
    }
  }
}
