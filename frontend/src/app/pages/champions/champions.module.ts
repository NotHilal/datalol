import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { ChampionsComponent } from './champions.component';
import { SharedModule } from '../../shared/shared.module';

const routes: Routes = [
  { path: '', component: ChampionsComponent }
];

@NgModule({
  declarations: [
    ChampionsComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class ChampionsModule { }
