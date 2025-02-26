import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { ChatbotService } from '../chatbot.service';

@Component({
  selector: 'app-ask',
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule, MatCardModule, MatInputModule],
  templateUrl: './ask.component.html',
  styleUrl: './ask.component.scss'
})
export class AskComponent {
  questions: { 
    question: string, 
    response: string, 
    relevantDocs: any[], 
    animatedSources: string[], 
    shownBulletPoints: boolean[],  // Controls when each bullet point appears
    showSourcesHeader: boolean 
  }[] = [];
  newQuestion: string = '';

  constructor(private dataService: DataService, private chatbotService: ChatbotService) {}

  ask(q: { 
    question: string, 
    response: string, 
    relevantDocs: any[], 
    animatedSources: string[], 
    shownBulletPoints: boolean[],
    showSourcesHeader: boolean 
  }) {
    if (!q.question.trim()) return;

    // Reset response, sources, and visibility flags
    q.response = '';
    q.animatedSources = [];
    q.shownBulletPoints = []; 
    q.showSourcesHeader = false; 

    this.dataService.askQuestion(q.question).subscribe(
      data => {
        const fullResponse = data.response;
        console.log(fullResponse);

        // Store relevant docs
        q.relevantDocs = data.relevant_docs;
        q.shownBulletPoints = Array(q.relevantDocs.length).fill(false); // Initially, hide all bullet points

        // Animate response first
        this.chatbotService.displayMessageWordByWord(fullResponse).subscribe({
          next: text => {
            q.response = text;
          },
          complete: () => {
            console.log("Bot response complete. Now showing 'Relevant Sources'...");
            this.showSources(q); // Show header first, then animate sources
          }
        });
      },
      error => console.error('Error:', error)
    );
  }

  showSources(q: { relevantDocs: any[], animatedSources: string[], shownBulletPoints: boolean[], showSourcesHeader: boolean }) {
    q.showSourcesHeader = true; // Show "Relevant Sources" header after response completes

    q.relevantDocs.forEach((doc, index) => {
      setTimeout(() => {
        q.shownBulletPoints[index] = true; // Show the bullet point
        q.animatedSources[index] = ''; // Start with an empty string

        this.chatbotService.displayMessageWordByWord(doc.metadata.source).subscribe({
          next: text => {
            q.animatedSources[index] = text;
          }
        });
      }, index * 1000); // Delay each bullet point and source animation by 1 second
    });
  }

  addQuestion() {
    if (this.newQuestion.trim()) {
      const newQ = { 
        question: this.newQuestion, 
        response: '', 
        relevantDocs: [], 
        animatedSources: [], 
        shownBulletPoints: [],
        showSourcesHeader: false 
      };
      this.questions.push(newQ);
      this.ask(newQ);
      this.newQuestion = '';
    }
  }
}
