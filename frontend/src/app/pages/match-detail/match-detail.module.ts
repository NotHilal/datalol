import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { MatchDetailComponent } from './match-detail.component';
import { SharedModule } from '../../shared/shared.module';

const routes: Routes = [
  { path: '', component: MatchDetailComponent }
];

@NgModule({
  declarations: [
    MatchDetailComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class MatchDetailModule { }
