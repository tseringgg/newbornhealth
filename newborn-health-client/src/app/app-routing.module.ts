import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { AppComponent } from "./app.component";
import { AskComponent } from "./ask/ask.component";
import { BrowserModule } from "@angular/platform-browser";

const routes: Routes = [
    {
        path: '',
        component: AppComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes), BrowserModule],
    exports: [RouterModule]
})
export class AppRoutingModule { }