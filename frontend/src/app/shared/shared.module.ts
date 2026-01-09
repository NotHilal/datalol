import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MatchCardComponent } from '../components/match-card/match-card.component';
import { PlayerStatsComponent } from '../components/player-stats/player-stats.component';
import { ChartComponent } from '../components/chart/chart.component';
import { PaginationComponent } from '../components/pagination/pagination.component';
import { TeamCompositionComponent } from '../components/team-composition/team-composition.component';

@NgModule({
  declarations: [
    MatchCardComponent,
    PlayerStatsComponent,
    ChartComponent,
    PaginationComponent,
    TeamCompositionComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    FormsModule
  ],
  exports: [
    MatchCardComponent,
    PlayerStatsComponent,
    ChartComponent,
    PaginationComponent,
    TeamCompositionComponent
  ]
})
export class SharedModule { }
