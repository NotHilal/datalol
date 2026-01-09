import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { StatisticsComponent } from './statistics.component';
import { SharedModule } from '../../shared/shared.module';

const routes: Routes = [
  { path: '', component: StatisticsComponent }
];

@NgModule({
  declarations: [
    StatisticsComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class StatisticsModule { }
