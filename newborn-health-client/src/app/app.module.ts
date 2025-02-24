import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { provideHttpClient } from '@angular/common/http';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatListModule } from '@angular/material/list';
import { MatSidenavModule } from '@angular/material/sidenav';
import { AdminComponent } from './admin/admin.component';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { AskComponent } from './ask/ask.component';
import { HomeComponent } from './home/home.component';
import { LearningComponent } from './learning/learning.component';

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
    MatListModule,
    MatExpansionModule,
    MatSidenavModule,
    
],
  providers: [provideHttpClient()],
  bootstrap: [AppComponent]
})
export class AppModule { }