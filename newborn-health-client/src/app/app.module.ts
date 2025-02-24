import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { AppComponent } from './app.component';
import { AskComponent } from './ask/ask.component';
import { provideHttpClient } from '@angular/common/http';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSidenavModule } from '@angular/material/sidenav';
import { HomeComponent } from './home/home.component';
import { LearningComponent } from './learning/learning.component';
import { AdminComponent } from './admin/admin.component';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'; 

@NgModule({
  declarations: [
    AppComponent,
    
    HomeComponent,
    LearningComponent,
    AdminComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AskComponent,
    // RouterModule,
    AppRoutingModule,
    BrowserAnimationsModule, // Add BrowserAnimationsModule to imports
    MatListModule,
    MatExpansionModule,
    MatSidenavModule,
    
],
  providers: [provideHttpClient()],
  bootstrap: [AppComponent]
})
export class AppModule { }