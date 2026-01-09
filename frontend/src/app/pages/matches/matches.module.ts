import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { MatchesComponent } from './matches.component';
import { SharedModule } from '../../shared/shared.module';

const routes: Routes = [
  { path: '', component: MatchesComponent }
];

@NgModule({
  declarations: [
    MatchesComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class MatchesModule { }
