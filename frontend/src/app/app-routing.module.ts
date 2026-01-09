import { NgModule } from '@angular/core';
import { RouterModule, Routes, PreloadAllModules } from '@angular/router';

import { DashboardComponent } from './pages/dashboard/dashboard.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },

  // Lazy-loaded routes - only load when user navigates to them
  {
    path: 'matches',
    loadChildren: () => import('./pages/matches/matches.module').then(m => m.MatchesModule)
  },
  {
    path: 'matches/:id',
    loadChildren: () => import('./pages/match-detail/match-detail.module').then(m => m.MatchDetailModule)
  },
  {
    path: 'players',
    loadChildren: () => import('./pages/players/players.module').then(m => m.PlayersModule)
  },
  {
    path: 'players/:puuid',
    loadChildren: () => import('./pages/player-detail/player-detail.module').then(m => m.PlayerDetailModule)
  },
  {
    path: 'statistics',
    loadChildren: () => import('./pages/statistics/statistics.module').then(m => m.StatisticsModule)
  },
  {
    path: 'champions',
    loadChildren: () => import('./pages/champions/champions.module').then(m => m.ChampionsModule)
  },
  {
    path: 'ml',
    loadChildren: () => import('./pages/ml/ml.module').then(m => m.MlModule)
  },

  { path: '**', redirectTo: '/dashboard' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    preloadingStrategy: PreloadAllModules,  // Preload after initial load
    initialNavigation: 'enabledBlocking'
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
