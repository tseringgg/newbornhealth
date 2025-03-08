import { Component, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { DataService } from '../data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { ChatbotService } from '../chatbot.service';
import { ThemeService } from '../theme.service';
import { MatIconModule } from '@angular/material/icon';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';


@Component({
  selector: 'app-ask',
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule, MatCardModule, MatInputModule, MatIconModule, MatSlideToggleModule],
  providers: [ThemeService],
  templateUrl: './ask.component.html',
  styleUrl: './ask.component.scss'
})
export class AskComponent implements AfterViewChecked {
  @ViewChild('messageContainer') messageContainer!: ElementRef; // Reference to the message container

  questions: { 
    question: string, 
    response: string, 
    relevantDocs: any[], 
    animatedSources: string[], 
    shownBulletPoints: boolean[],  
    showSourcesHeader: boolean,
    isThinking: boolean,
    responseComplete: boolean,
    showPlaceholder: boolean, // NEW: Controls extra whitespace
    placeholderHeight: number
  }[] = [];
  
  newQuestion: string = '';
  private shouldScroll: boolean = false; // Tracks when to scroll

  constructor(private dataService: DataService, private chatbotService: ChatbotService, public themeService: ThemeService) {}

  ngAfterViewChecked() {
    if (this.shouldScroll) {
      this.scrollToLatestQuestion();
      this.shouldScroll = false;
    }
  }

  ask(q: { 
    question: string, 
    response: string, 
    relevantDocs: any[], 
    animatedSources: string[], 
    shownBulletPoints: boolean[],
    showSourcesHeader: boolean, 
    isThinking: boolean, 
    responseComplete: boolean,
    showPlaceholder: boolean,
    placeholderHeight: number
  }) {
    if (!q.question.trim()) return;
  
    // Reset response state
    q.response = '';
    q.animatedSources = [];
    q.shownBulletPoints = []; 
    q.showSourcesHeader = false; 
    q.isThinking = true; 
    q.responseComplete = false;
    q.showPlaceholder = true; // Keep whitespace static
  
    // this.questions.push({ ...q, placeholderHeight: 500 });
    this.questions.push(q);
    this.shouldScroll = true;
  
    this.dataService.askQuestion(q.question).subscribe(
      data => {
        const fullResponse = data.response;
        console.log(fullResponse);
  
        q.relevantDocs = data.relevant_docs;
        q.shownBulletPoints = Array(q.relevantDocs.length).fill(false);
  
        // Start animating response
        this.chatbotService.displayMessageWordByWord(fullResponse).subscribe({
          next: text => {
            q.response = text;
          },
          complete: () => {
            q.isThinking = false;
            q.responseComplete = true;
            this.showSources(q);
          }
        });
      },
      error => {
        console.error('Error:', error);
        q.isThinking = false;
      }
    );
  }
  
  showSources(q: { relevantDocs: any[], animatedSources: string[], shownBulletPoints: boolean[], showSourcesHeader: boolean, showPlaceholder: boolean }) {
    q.showSourcesHeader = true;

    q.relevantDocs.forEach((doc, index) => {
      setTimeout(() => {
        q.shownBulletPoints[index] = true;
        q.animatedSources[index] = ''; // Reset for each doc

        // Format the Source Text with Page Number
        const sourceText = `${doc.metadata.source}, Page ${doc.metadata.page_number}`;

        this.chatbotService.displayMessageWordByWord(sourceText).subscribe({
          next: text => {
            q.animatedSources[index] = text;
          },
          complete: () => {
            console.log(`Source ${index + 1} complete.`);
            if (index === q.relevantDocs.length - 1) {
              q.showPlaceholder = false;
            }
          }
        });
      }, index * 500);
    });
  }
  
  /** Controls when the input form should appear */
  shouldShowInput(): boolean {
    if (this.questions.length === 0) return true; // Show input if no questions exist
    const lastQ = this.questions[this.questions.length - 1];
    return lastQ.responseComplete && !lastQ.showPlaceholder; // Only show after response & sources are done
  }
  
  

  addQuestion() {
    if (this.newQuestion.trim()) {
      const newQ = { 
        question: this.newQuestion, 
        response: '', 
        relevantDocs: [], 
        animatedSources: [], 
        shownBulletPoints: [],
        showSourcesHeader: false, 
        isThinking: false, 
        responseComplete: false,
        showPlaceholder: true, // Added
        placeholderHeight: 500 // Initial placeholder height
      };
      this.ask(newQ);
      this.newQuestion = '';
    }
  }

  private scrollToLatestQuestion() {
    setTimeout(() => {
      if (this.messageContainer) {
        const messageElements = this.messageContainer.nativeElement.children;
        if (messageElements.length > 0) {
          const latestMessage = messageElements[messageElements.length - 1];
  
          // Scroll with an offset to compensate for the header
          const OFFSET = 140; // Adjust based on header height
          const targetPosition = latestMessage.getBoundingClientRect().top + window.scrollY - OFFSET;
  
          window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        }
      }
    }, 150); // Small delay to ensure DOM updates
  }
  
  
}
