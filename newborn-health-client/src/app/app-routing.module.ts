import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { AppComponent } from "./app.component";
import { AskComponent } from "./ask/ask.component";
import { BrowserModule } from "@angular/platform-browser";
import { HomeComponent } from "./home/home.component";
import { AdminComponent } from "./admin/admin.component";
import { LearningComponent } from "./learning/learning.component";

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent
    },
    {
        path: 'learning',
        component: LearningComponent
    },
    {
        path: 'admin',
        component: AdminComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes), BrowserModule],
    exports: [RouterModule]
})
export class AppRoutingModule { }