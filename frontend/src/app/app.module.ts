import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Services
import { ApiService } from './services/api.service';
import { MatchService } from './services/match.service';
import { PlayerService } from './services/player.service';
import { StatisticsService } from './services/statistics.service';
import { MlService } from './services/ml.service';

// Components
import { NavbarComponent } from './components/navbar/navbar.component';
import { MatchCardComponent } from './components/match-card/match-card.component';
import { PlayerStatsComponent } from './components/player-stats/player-stats.component';
import { ChartComponent } from './components/chart/chart.component';
import { PaginationComponent } from './components/pagination/pagination.component';

// Pages
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { MatchesComponent } from './pages/matches/matches.component';
import { MatchDetailComponent } from './pages/match-detail/match-detail.component';
import { PlayersComponent } from './pages/players/players.component';
import { PlayerDetailComponent } from './pages/player-detail/player-detail.component';
import { StatisticsComponent } from './pages/statistics/statistics.component';
import { MlComponent } from './pages/ml/ml.component';

@NgModule({
  declarations: [
    AppComponent,
    // Components
    NavbarComponent,
    MatchCardComponent,
    PlayerStatsComponent,
    ChartComponent,
    PaginationComponent,
    // Pages
    DashboardComponent,
    MatchesComponent,
    MatchDetailComponent,
    PlayersComponent,
    PlayerDetailComponent,
    StatisticsComponent,
    MlComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule
  ],
  providers: [
    ApiService,
    MatchService,
    PlayerService,
    StatisticsService,
    MlService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
