import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TinymcecompComponent } from './tinymcecomp/tinymcecomp.component';

const routes: Routes = [
  // {path: 'result', component: TinymcecompComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
