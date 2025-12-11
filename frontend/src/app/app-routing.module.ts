import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { MatchesComponent } from './pages/matches/matches.component';
import { MatchDetailComponent } from './pages/match-detail/match-detail.component';
import { PlayersComponent } from './pages/players/players.component';
import { PlayerDetailComponent } from './pages/player-detail/player-detail.component';
import { StatisticsComponent } from './pages/statistics/statistics.component';
import { MlComponent } from './pages/ml/ml.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'matches', component: MatchesComponent },
  { path: 'matches/:id', component: MatchDetailComponent },
  { path: 'players', component: PlayersComponent },
  { path: 'players/:puuid', component: PlayerDetailComponent },
  { path: 'statistics', component: StatisticsComponent },
  { path: 'ml', component: MlComponent },
  { path: '**', redirectTo: '/dashboard' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
