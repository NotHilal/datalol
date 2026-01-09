import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { PlayersComponent } from './players.component';
import { SharedModule } from '../../shared/shared.module';

const routes: Routes = [
  { path: '', component: PlayersComponent }
];

@NgModule({
  declarations: [
    PlayersComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    SharedModule,
    RouterModule.forChild(routes)
  ]
})
export class PlayersModule { }
