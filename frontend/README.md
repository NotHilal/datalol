# Frontend - Angular Application

Angular frontend for League of Legends Match Analytics.

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Edit `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api/v1'
};
```

### 3. Run Development Server

```bash
npm start
# or
ng serve
```

Navigate to `http://localhost:4200`

## Project Structure

```
frontend/src/
├── app/
│   ├── components/        # Reusable components
│   │   ├── match-card/
│   │   ├── player-stats/
│   │   └── chart/
│   ├── pages/            # Page components
│   │   ├── dashboard/
│   │   ├── matches/
│   │   ├── players/
│   │   └── statistics/
│   ├── services/         # API services
│   │   ├── api.service.ts
│   │   ├── match.service.ts
│   │   ├── player.service.ts
│   │   └── statistics.service.ts
│   ├── models/           # TypeScript interfaces
│   │   ├── match.model.ts
│   │   ├── player.model.ts
│   │   └── statistics.model.ts
│   ├── shared/           # Shared modules
│   │   ├── pipes/
│   │   └── directives/
│   ├── app.module.ts
│   └── app-routing.module.ts
├── assets/               # Static assets
├── environments/         # Environment configs
└── styles.scss          # Global styles
```

## Available Scripts

### Development
```bash
npm start              # Start dev server
npm run build          # Build for production
npm run build:dev      # Build for development
npm test              # Run tests
npm run lint          # Lint code
```

### Build
```bash
npm run build
# Output in dist/
```

## Creating Components

### Generate Component
```bash
ng generate component components/match-card
ng generate component pages/dashboard
```

### Generate Service
```bash
ng generate service services/match
```

### Generate Model
```bash
ng generate interface models/match
```

## Services

### ApiService
Base service for HTTP requests:
```typescript
constructor(private api: ApiService) {}

this.api.get<T>(endpoint, params);
this.api.post<T>(endpoint, body);
```

### MatchService
```typescript
getMatches(page, pageSize)
getMatchById(matchId)
getMatchesByPlayer(playerName)
getMatchesByChampion(championName)
```

### PlayerService
```typescript
getPlayers(page, pageSize, tier?, rank?)
getPlayerByPuuid(puuid)
getLeaderboard(limit)
getTierDistribution()
```

### StatisticsService
```typescript
getChampionStatistics(championName?)
getPlayerStatistics(playerName)
getTeamStatistics()
getOverviewStatistics()
```

## Routing

Routes are defined in `app-routing.module.ts`:

```typescript
const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'matches', component: MatchListComponent },
  { path: 'matches/:id', component: MatchDetailComponent },
  { path: 'players', component: PlayerListComponent },
  { path: 'statistics', component: StatisticsComponent },
];
```

## Styling

### Global Styles
Located in `src/styles.scss`

### Component Styles
Each component has its own `.scss` file

### Utility Classes
```scss
.container     # Max-width container
.card         # Card layout
.btn          # Button styles
.btn-primary  # Primary button
.loading      # Loading indicator
.error        # Error message
```

## Data Flow

1. **Component** requests data from **Service**
2. **Service** calls **ApiService** with endpoint
3. **ApiService** makes HTTP request to **Flask API**
4. **Response** flows back through services to **Component**
5. **Component** updates view with data

## Development Guidelines

### TypeScript
- Use strict type checking
- Define interfaces for all data models
- Avoid `any` type

### Components
- Keep components focused and small
- Use OnPush change detection when possible
- Implement OnDestroy for cleanup

### Services
- Use RxJS operators for data transformation
- Handle errors gracefully
- Cache data when appropriate

### Styling
- Use SCSS features (variables, mixins)
- Follow BEM naming convention
- Make responsive designs

## Testing

### Unit Tests
```bash
npm test
```

### E2E Tests
```bash
npm run e2e
```

## Building for Production

```bash
npm run build
```

### Deploy to Server
```bash
# Copy dist/ folder to web server
# Configure web server to serve index.html for all routes
```

### Environment Variables
Update `environment.prod.ts` for production:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.yourdomain.com/api/v1'
};
```

## Troubleshooting

### CORS Issues
Ensure Flask backend has CORS enabled for your frontend URL.

### API Connection
Check `apiUrl` in environment file matches backend URL.

### Build Errors
```bash
rm -rf node_modules package-lock.json
npm install
```

## Resources

- [Angular Documentation](https://angular.io/docs)
- [Angular CLI](https://angular.io/cli)
- [RxJS Documentation](https://rxjs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
