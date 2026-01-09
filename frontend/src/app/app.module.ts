import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SharedModule } from './shared/shared.module';

// Services
import { ApiService } from './services/api.service';
import { MatchService } from './services/match.service';
import { PlayerService } from './services/player.service';
import { StatisticsService } from './services/statistics.service';
import { MlService } from './services/ml.service';

// Core Components (always loaded)
import { NavbarComponent } from './components/navbar/navbar.component';

// Dashboard (eagerly loaded - it's the landing page)
import { DashboardComponent } from './pages/dashboard/dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    DashboardComponent  // Only dashboard loaded upfront
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule,
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
