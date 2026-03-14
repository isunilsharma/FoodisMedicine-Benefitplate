<p align="center">
  <h1 align="center">BenefitPlate</h1>
  <p align="center">
    <strong>Find food and nutrition benefits you may qualify for</strong>
  </p>
  <p align="center">
    A full-stack application that matches users to food benefit programs based on ZIP code, income, and health criteria using a deterministic eligibility engine.
  </p>
</p>

---

## Overview

BenefitPlate is an open-source eligibility navigator for food and nutrition assistance programs in California. Users answer a short questionnaire and receive personalized results showing programs they likely qualify for, along with downloadable PDF checklists and next-step guidance.

### Key Features

- **ZIP-based geographic matching** — Programs filtered by county and state using HUD USPS ZIP-County crosswalk data
- **Multi-step eligibility questionnaire** — Guided flow covering income, insurance, household size, age, and health conditions
- **Deterministic rule engine** — Transparent, auditable matching logic (no black-box ML)
- **AI-powered explanations** — Optional LLM integration for plain-English eligibility summaries
- **PDF checklist generation** — Downloadable document with required paperwork and application links
- **Admin console** — Program management (CRUD), analytics dashboard, and review workflows
- **OAuth authentication** — Secure sign-in with session-based auth and cookie management

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│              React + Tailwind CSS + Shadcn/UI                │
│                                                              │
│  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────────┐ │
│  │ Landing   │ │ Eligibility  │ │ Programs │ │   Admin    │ │
│  │ Page      │ │ Questionnaire│ │ Browser  │ │  Console   │ │
│  └──────────┘ └──────────────┘ └──────────┘ └────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (/api)
┌──────────────────────┴──────────────────────────────────────┐
│                        Backend                               │
│                    FastAPI + Python                           │
│                                                              │
│  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────────┐ │
│  │   Auth   │ │  Eligibility │ │Geography │ │    PDF     │ │
│  │  Module  │ │    Engine    │ │  Lookup  │ │ Generator  │ │
│  └──────────┘ └──────────────┘ └──────────┘ └────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                       MongoDB                                │
│  Collections: programs, program_rules, zip_county_mapping,   │
│  users, user_sessions, analytics_events, user_saved_results  │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, React Router, Tailwind CSS, Shadcn/UI, Axios, Lucide Icons |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, Motor (async MongoDB driver) |
| **Database** | MongoDB 6+ |
| **PDF Generation** | ReportLab |
| **LLM (optional)** | OpenAI API (GPT-4o or compatible) |
| **Authentication** | OAuth 2.0 with session-based auth |

---

## Prerequisites

- **Python** 3.11 or higher
- **Node.js** 18 or higher
- **MongoDB** 6.0 or higher (running locally or via MongoDB Atlas)
- **OpenAI API key** (optional, for AI-powered explanations)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/benefitplate.git
cd benefitplate
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `backend/.env` with your configuration:

```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="benefitplate"
CORS_ORIGINS="http://localhost:3000"
OPENAI_API_KEY=your_openai_api_key_here    # Optional
LLM_MODEL=gpt-4o                           # Optional
AUTH_SERVICE_URL=your_auth_service_url      # Required for OAuth
ADMIN_EMAIL=admin@example.com
```

> **Note:** If `OPENAI_API_KEY` is not set, the app falls back to rule-based explanations. All core functionality works without it.

Start the backend:

```bash
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

The server will automatically seed the database on first startup with:
- California ZIP code mappings (2,500+ ZIP codes)
- Sample food benefit programs with eligibility rules

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
yarn install

# Configure environment
cp .env.example .env
```

Edit `frontend/.env`:

```env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_AUTH_URL=https://your-auth-provider.com
```

Start the frontend:

```bash
yarn start
```

The app will open at [http://localhost:3000](http://localhost:3000).

---

## Authentication Setup

BenefitPlate uses OAuth 2.0 for authentication. The auth flow works as follows:

1. User clicks "Sign In" and is redirected to the OAuth provider
2. After authentication, the provider redirects back with a `session_id` in the URL hash
3. The frontend exchanges the `session_id` for a `session_token` via the backend
4. The `session_token` is stored as an httpOnly cookie for subsequent requests

### Configuring Your Own OAuth Provider

To use your own OAuth provider, you need to implement a session exchange endpoint that:

1. **Accepts** a GET request with an `X-Session-ID` header
2. **Returns** JSON with `email`, `name`, `picture` (optional), and `session_token` fields

Set the endpoint URL in `AUTH_SERVICE_URL` (backend) and the login page URL in `REACT_APP_AUTH_URL` (frontend).

### Admin Access

Set the `ADMIN_EMAIL` environment variable to grant admin privileges to a specific user. The admin console is accessible at `/admin` after sign-in.

---

## Project Structure

```
benefitplate/
├── backend/
│   ├── server.py              # FastAPI app, all API endpoints
│   ├── auth.py                # OAuth session exchange & user management
│   ├── models.py              # Pydantic data models
│   ├── eligibility_engine.py  # Deterministic rule-based matching
│   ├── geography.py           # ZIP code to county/state lookup
│   ├── pdf_generator.py       # ReportLab PDF checklist generation
│   ├── llm_explanations.py    # OpenAI-powered program explanations
│   ├── analytics.py           # Event tracking utilities
│   ├── seed_data.py           # Program & rules database seeder
│   ├── seed_california_zips.py # California ZIP code seeder
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js             # Root component & routing
│   │   ├── components/
│   │   │   ├── AuthCallback.js  # OAuth callback handler
│   │   │   ├── Navigation.js    # Top nav bar
│   │   │   ├── Footer.js        # Site footer
│   │   │   ├── ProtectedRoute.js # Auth guard wrapper
│   │   │   └── ui/              # Shadcn/UI components
│   │   ├── contexts/
│   │   │   └── AuthContext.js   # Global auth state
│   │   ├── pages/
│   │   │   ├── LandingPage.js
│   │   │   ├── CheckEligibilityPage.js
│   │   │   ├── ResultsPage.js
│   │   │   ├── ProgramsPage.js
│   │   │   ├── ProgramDetailPage.js
│   │   │   ├── DashboardPage.js
│   │   │   ├── AdminPage.js
│   │   │   └── HelpPage.js
│   │   └── utils/
│   │       └── api.js           # Axios API client
│   ├── package.json
│   └── .env.example
└── .gitignore
```

---

## API Reference

All endpoints are prefixed with `/api`.

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/geography/lookup` | ZIP code to county/state lookup |
| `POST` | `/api/eligibility/evaluate` | Evaluate eligibility for programs |
| `GET` | `/api/programs` | List all active programs (filterable) |
| `GET` | `/api/programs/:id` | Get program details |

### Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/session` | Exchange session_id for session_token |
| `GET` | `/api/auth/me` | Get current authenticated user |
| `POST` | `/api/auth/logout` | Logout and clear session |

### Protected Endpoints (requires authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/user/save-result` | Save eligibility results |
| `GET` | `/api/user/saved-results` | Get user's saved results |
| `POST` | `/api/user/generate-checklist-pdf` | Generate PDF checklist |

### Admin Endpoints (requires admin role)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/admin/programs` | List all programs (any status) |
| `POST` | `/api/admin/programs` | Create a new program |
| `PUT` | `/api/admin/programs/:id` | Update a program |
| `DELETE` | `/api/admin/programs/:id` | Delete a program |
| `GET` | `/api/admin/programs/needs-review` | Programs needing re-verification |
| `GET` | `/api/admin/analytics` | Usage analytics dashboard data |

### Example: Evaluate Eligibility

```bash
curl -X POST http://localhost:8001/api/eligibility/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "zip_code": "90001",
    "answers": {
      "enrolled_medicaid": "Yes",
      "enrolled_snap": "No",
      "household_size": 3,
      "income_band": "Under $25,000",
      "age_range": "18-59",
      "pregnancy": "No",
      "health_conditions": ["Diabetes"],
      "has_case_manager": "No"
    }
  }'
```

---

## Database Schema

### `programs`
```json
{
  "program_id": "prog_abc123",
  "program_name": "California Fresh Produce Rx",
  "benefit_type": "produce_rx",
  "geo_scope": "state",
  "state": "California",
  "county": null,
  "status": "active",
  "how_to_apply_url": "https://example.com/apply",
  "contact_phone": "1-800-555-0100",
  "source_urls": ["https://example.com"],
  "effective_start": "2024-01-01T00:00:00Z",
  "last_verified_at": "2024-06-01T00:00:00Z"
}
```

### `program_rules`
```json
{
  "program_id": "prog_abc123",
  "eligibility_conditions_json": {
    "match_logic": {
      "all_of": [
        {"field": "enrolled_medicaid", "operator": "eq", "value": "Yes"}
      ]
    }
  },
  "document_checklist_json": {
    "required": ["Photo ID", "Proof of income"],
    "optional": ["Medical referral"]
  },
  "requires_medicaid": true,
  "income_fpl_bands_allowed": ["Under $25,000", "$25,000 - $35,000"]
}
```

### `zip_county_mapping`
```json
{
  "zip_code": "90001",
  "county": "Los Angeles County",
  "state": "California",
  "state_code": "CA"
}
```

---

## Eligibility Engine

The matching engine (`eligibility_engine.py`) uses a deterministic, rule-based approach:

1. **Geographic filtering** — Only programs matching the user's state/county are considered
2. **Condition evaluation** — Each program's rules are checked against questionnaire answers
3. **Classification** — Programs are sorted into three tiers:
   - **Likely Eligible** — All required conditions met
   - **Possibly Eligible** — Most conditions met, some uncertain (e.g., "Not sure" answers)
   - **Community Resources** — Programs with minimal or no eligibility requirements

### Supported Rule Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equals | `{"field": "enrolled_medicaid", "operator": "eq", "value": "Yes"}` |
| `neq` | Not equals | `{"field": "pregnancy", "operator": "neq", "value": "Yes"}` |
| `in` | Value in list | `{"field": "age_range", "operator": "in", "value": ["18-59", "60+"]}` |
| `contains` | List contains value | `{"field": "health_conditions", "operator": "contains", "value": "Diabetes"}` |
| `any_true` | Any value matches | `{"field": "health_conditions", "operator": "any_true", "value": ["Diabetes", "Heart disease"]}` |

### Rule Logic

Rules support `all_of` (AND), `any_of` (OR), and `none_of` (NOT) condition groups:

```json
{
  "match_logic": {
    "all_of": [
      {"field": "enrolled_medicaid", "operator": "eq", "value": "Yes"},
      {"field": "income_band", "operator": "in", "value": ["Under $25,000", "$25,000 - $35,000"]}
    ],
    "any_of": [
      {"field": "health_conditions", "operator": "contains", "value": "Diabetes"},
      {"field": "health_conditions", "operator": "contains", "value": "Heart disease"}
    ]
  }
}
```

---

## Adding Programs

### Via Admin Console

1. Sign in with the admin email
2. Navigate to `/admin`
3. Click "Add Program" and fill in the form
4. Set eligibility rules using JSON format

### Via Database Seeder

Edit `backend/seed_data.py` to add programs programmatically:

```python
{
    "program_id": "prog_my_program",
    "program_name": "My New Program",
    "benefit_type": "produce_rx",  # Options: produce_rx, mtg, mtm, pantry, snap_support, nutrition_coaching, other
    "geo_scope": "state",          # Options: national, state, county, city, zip
    "state": "California",
    "status": "active",
    "how_to_apply_url": "https://example.com/apply",
    "contact_phone": "1-800-555-0100"
}
```

Run the seeder:

```bash
cd backend
python -c "import asyncio; from seed_data import seed_programs; from motor.motor_asyncio import AsyncIOMotorClient; asyncio.run(seed_programs(AsyncIOMotorClient('mongodb://localhost:27017')['benefitplate']))"
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URL` | Yes | MongoDB connection string |
| `DB_NAME` | Yes | MongoDB database name |
| `CORS_ORIGINS` | Yes | Comma-separated allowed origins |
| `AUTH_SERVICE_URL` | Yes | OAuth session exchange endpoint |
| `ADMIN_EMAIL` | Yes | Email address with admin privileges |
| `OPENAI_API_KEY` | No | OpenAI API key for LLM explanations |
| `LLM_MODEL` | No | OpenAI model name (default: `gpt-4o`) |

### Frontend (`frontend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `REACT_APP_BACKEND_URL` | Yes | Backend API URL (no trailing slash) |
| `REACT_APP_AUTH_URL` | Yes | OAuth login page URL |

---

## Deployment

### Docker (Recommended)

```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

```dockerfile
# Frontend
FROM node:18-alpine
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile
COPY frontend/ .
RUN yarn build
# Serve with nginx or any static file server
```

### Environment Notes

- Backend listens on port **8001** by default
- Frontend expects the backend URL via `REACT_APP_BACKEND_URL`
- MongoDB must be accessible from the backend container
- Set `CORS_ORIGINS` to your frontend's production URL

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

### Code Style

- **Backend:** Follow PEP 8 conventions. Use type hints for function signatures.
- **Frontend:** Use functional components with hooks. Follow the existing Shadcn/UI component patterns.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- ZIP code data sourced from the [HUD USPS ZIP-County Crosswalk](https://www.huduser.gov/portal/datasets/usps_crosswalk.html)
- UI components built with [Shadcn/UI](https://ui.shadcn.com/)
- Program data compiled from California state health and nutrition program directories
