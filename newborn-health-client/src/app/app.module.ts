import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { AppComponent } from './app.component';
import { AskComponent } from './ask/ask.component';
import { provideHttpClient } from '@angular/common/http';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { HomeComponent } from './home/home.component';
import { LearningComponent } from './learning/learning.component';
import { AdminComponent } from './admin/admin.component';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'; 
import { ThemeService } from './theme.service';
import { MarkdownModule } from 'ngx-markdown';

@NgModule({
  declarations: [
    AppComponent,
    
    HomeComponent,
    LearningComponent,
    AdminComponent,
    // AskComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    // RouterModule,
    AppRoutingModule,
    BrowserAnimationsModule, // Add BrowserAnimationsModule to imports
    MatListModule,
    MatExpansionModule,
    MatSidenavModule,
    MatIconModule,
    MarkdownModule.forRoot(),
    
],
  providers: [provideHttpClient(), ThemeService],
  bootstrap: [AppComponent]
})
export class AppModule { }