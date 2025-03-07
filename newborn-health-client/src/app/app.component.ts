import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AskComponent } from "./ask/ask.component";
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: false,
  //imports: [RouterOutlet, AskComponent, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'] // Corrected property name
})
export class AppComponent {
  title = 'newborn-health-client';
}
