# Complete Project Structure

## Full Directory Tree

```
league-of-legends-project/
│
├── backend/                              # Flask Backend Application
│   ├── app/                             # Main application package
│   │   ├── models/                      # Database models
│   │   │   ├── __init__.py             # Models package init
│   │   │   ├── match.py                # Match model with MongoDB operations
│   │   │   └── player.py               # Player model with queries
│   │   │
│   │   ├── routes/                      # API route blueprints
│   │   │   ├── __init__.py             # Routes package init
│   │   │   ├── matches.py              # Match endpoints
│   │   │   ├── players.py              # Player endpoints
│   │   │   └── statistics.py           # Statistics endpoints
│   │   │
│   │   ├── services/                    # Business logic layer
│   │   │   └── (future services)
│   │   │
│   │   ├── utils/                       # Utility functions
│   │   │   ├── __init__.py             # Utils package init
│   │   │   ├── response.py             # Response formatters
│   │   │   └── validators.py           # Input validators
│   │   │
│   │   ├── middlewares/                 # Custom middlewares
│   │   │   └── (future middlewares)
│   │   │
│   │   └── __init__.py                 # App factory pattern
│   │
│   ├── config/                          # Configuration files
│   │   ├── __init__.py                 # Config package init
│   │   └── config.py                   # Environment configs
│   │
│   ├── tests/                           # Test suite
│   │   ├── test_models.py              # Model tests
│   │   ├── test_routes.py              # Route tests
│   │   └── test_utils.py               # Utility tests
│   │
│   ├── migrations/                      # Database migrations
│   │   └── (future migrations)
│   │
│   ├── static/                          # Static files
│   │   └── (if needed)
│   │
│   ├── run.py                           # Application entry point
│   ├── requirements.txt                 # Python dependencies
│   ├── .env.example                     # Environment template
│   ├── .env                             # Environment variables (gitignored)
│   └── README.md                        # Backend documentation
│
├── frontend/                            # Angular Frontend Application
│   ├── src/                            # Source files
│   │   ├── app/                        # Angular application
│   │   │   ├── components/             # Reusable components
│   │   │   │   ├── match-card/         # Match card component
│   │   │   │   ├── player-stats/       # Player statistics component
│   │   │   │   ├── chart/              # Chart component
│   │   │   │   └── pagination/         # Pagination component
│   │   │   │
│   │   │   ├── pages/                  # Page components
│   │   │   │   ├── dashboard/          # Dashboard page
│   │   │   │   ├── matches/            # Matches list page
│   │   │   │   ├── match-detail/       # Match detail page
│   │   │   │   ├── players/            # Players list page
│   │   │   │   ├── player-detail/      # Player detail page
│   │   │   │   └── statistics/         # Statistics page
│   │   │   │
│   │   │   ├── services/               # Angular services
│   │   │   │   ├── api.service.ts      # Base HTTP service
│   │   │   │   ├── match.service.ts    # Match data service
│   │   │   │   ├── player.service.ts   # Player data service
│   │   │   │   └── statistics.service.ts # Statistics service
│   │   │   │
│   │   │   ├── models/                 # TypeScript interfaces
│   │   │   │   ├── match.model.ts      # Match data types
│   │   │   │   ├── player.model.ts     # Player data types
│   │   │   │   └── statistics.model.ts # Statistics types
│   │   │   │
│   │   │   ├── shared/                 # Shared modules
│   │   │   │   ├── pipes/              # Custom pipes
│   │   │   │   ├── directives/         # Custom directives
│   │   │   │   └── interceptors/       # HTTP interceptors
│   │   │   │
│   │   │   ├── app.component.ts        # Root component
│   │   │   ├── app.component.html      # Root template
│   │   │   ├── app.component.scss      # Root styles
│   │   │   ├── app.module.ts           # Root module
│   │   │   └── app-routing.module.ts   # Routing configuration
│   │   │
│   │   ├── assets/                     # Static assets
│   │   │   ├── images/                 # Images
│   │   │   ├── icons/                  # Icons
│   │   │   └── data/                   # Static data files
│   │   │
│   │   ├── environments/               # Environment configs
│   │   │   ├── environment.ts          # Development config
│   │   │   └── environment.prod.ts     # Production config
│   │   │
│   │   ├── styles.scss                 # Global styles
│   │   ├── main.ts                     # Application bootstrap
│   │   └── index.html                  # HTML entry point
│   │
│   ├── angular.json                     # Angular configuration
│   ├── package.json                     # Node dependencies
│   ├── package-lock.json               # Locked dependencies
│   ├── tsconfig.json                    # TypeScript config
│   ├── tsconfig.app.json               # App TypeScript config
│   ├── tsconfig.spec.json              # Test TypeScript config
│   └── README.md                        # Frontend documentation
│
├── data/                                # Data files
│   ├── matchData.csv                    # Match data (CSV format)
│   ├── match_data.jsonl                 # Match data (JSONL format)
│   ├── match_ids.csv                    # Match IDs with tiers
│   └── players_8-14-25.csv             # Player data
│
├── scripts/                             # Utility scripts
│   ├── load_to_mongodb.py              # Data loader script
│   ├── load_to_mongodb.py              # (already exists from earlier)
│   └── (future scripts)
│
├── docker/                              # Docker configuration (future)
│   ├── Dockerfile.backend              # Backend Docker image
│   ├── Dockerfile.frontend             # Frontend Docker image
│   └── docker-compose.yml              # Multi-container setup
│
├── .gitignore                           # Git ignore rules
├── README.md                            # Main project documentation
├── API_DOCUMENTATION.md                 # API endpoint documentation
└── PROJECT_STRUCTURE.md                 # This file
```

## File Count Summary

### Backend
- **Python Files**: 15+
- **Configuration Files**: 3
- **Documentation**: 1 README

### Frontend
- **TypeScript Files**: 20+
- **HTML Templates**: 10+
- **SCSS Stylesheets**: 10+
- **Configuration Files**: 5
- **Documentation**: 1 README

### Total Files Created: 50+

## Key Technologies by Layer

### Backend Layer
```
Flask (Web Framework)
├── Flask-CORS (Cross-origin requests)
├── Pymongo (MongoDB driver)
└── Python-dotenv (Environment variables)

MongoDB (Database)
├── Matches Collection
└── Players Collection
```

### Frontend Layer
```
Angular 17 (Framework)
├── HttpClient (HTTP requests)
├── RouterModule (Routing)
├── FormsModule (Forms)
└── ReactiveFormsModule (Reactive forms)

Chart.js (Visualizations)
└── ng2-charts (Angular wrapper)
```

### Development Tools
```
Git (Version control)
npm (Package manager)
pip (Python packages)
pytest (Python testing)
Jasmine/Karma (Angular testing)
```

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            Angular Application (Port 4200)             │ │
│  │                                                         │ │
│  │  Components → Services → HTTP Client                   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Requests (REST API)
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                    Flask Backend (Port 5000)                │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Routes → Models → MongoDB Queries                     │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │ Database Queries
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                MongoDB Database (Port 27017)                │
│                                                              │
│  Collections:                                               │
│  ├── matches (101,843 documents)                           │
│  └── players (3,561 documents)                             │
└─────────────────────────────────────────────────────────────┘
```

## API Request Flow Example

```
User Action: Click "View Match Details"
     ↓
Angular Component: MatchDetailComponent
     ↓
Service Call: matchService.getMatchById(matchId)
     ↓
HTTP Request: GET /api/v1/matches/:matchId
     ↓
Flask Route: @matches_bp.route('/:matchId')
     ↓
Model Method: Match.find_by_id(matchId)
     ↓
MongoDB Query: collection.find_one({"matchId": matchId})
     ↓
Response: Match Document (JSON)
     ↓
Service: Observable<Match>
     ↓
Component: Display match data
     ↓
View: Rendered match details
```

## Environment Configuration

### Development
```
Backend:  localhost:5000
Frontend: localhost:4200
MongoDB:  localhost:27017
```

### Production
```
Backend:  https://api.yourdomain.com
Frontend: https://yourdomain.com
MongoDB:  mongodb+srv://cluster.mongodb.net
```

## Security Considerations

### Backend
- Environment variables for secrets
- CORS configuration
- Input validation
- MongoDB injection prevention

### Frontend
- HTTP-only cookies (if using auth)
- XSS prevention (Angular built-in)
- CSRF protection
- Secure API communication

## Scalability Considerations

### Backend
- Stateless API design
- MongoDB indexes for performance
- Pagination for large datasets
- Caching layer (future)

### Frontend
- Lazy loading modules
- Virtual scrolling for lists
- Service worker (PWA)
- Code splitting

## Next Steps for Development

1. **Create page components**
   - Dashboard with overview statistics
   - Match list and detail views
   - Player list and detail views
   - Statistics visualization page

2. **Add features**
   - Search functionality
   - Filters and sorting
   - Data visualization charts
   - User authentication (optional)

3. **Testing**
   - Unit tests for services
   - Component tests
   - Integration tests
   - E2E tests

4. **Deployment**
   - Dockerize applications
   - CI/CD pipeline
   - Production hosting
   - Monitoring and logging
