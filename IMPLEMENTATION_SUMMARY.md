# BenefitPlate - Food Is Medicine Eligibility Navigator

## Application Overview
BenefitPlate helps users discover Food Is Medicine and food support programs they may qualify for based on ZIP code and a short questionnaire.

## Tech Stack
- **Backend**: FastAPI + MongoDB (Motor async driver)
- **Frontend**: React 19 + Tailwind CSS + Shadcn/UI
- **Auth**: Emergent-managed Google OAuth
- **LLM**: OpenAI GPT-5.2 (via Emergent LLM key)
- **PDF**: ReportLab

## Features Implemented

### ✅ Backend APIs (All Functional)
- **Authentication** (`/api/auth/*`)
  - Session exchange, user info, logout
  - Cookie-based session management
  - Admin role checking (sunilbg100@gmail.com)

- **Geography** (`/api/geography/*`)
  - ZIP → County → State lookup
  - 20 sample ZIP codes seeded

- **Eligibility** (`/api/eligibility/*`)
  - Deterministic rule-based matching (NO LLM)
  - Categorizes: Likely, Possibly, Community
  - 9-question questionnaire evaluation

- **Programs** (`/api/programs/*`)
  - List/filter programs
  - Get program details
  - 6 sample programs seeded

- **User** (`/api/user/*`)
  - Save eligibility results
  - Get saved results
  - Generate PDF checklist

- **Admin** (`/api/admin/*`)
  - CRUD programs
  - Manage eligibility rules
  - View programs needing review

### ✅ Frontend Pages (All Built)
1. **Landing Page** - Hero, features, "Why different" section
2. **Check Eligibility** - 9-step questionnaire with progress
3. **Results** - Categorized programs with save/download
4. **Program Directory** - Browse/search with filters
5. **Program Detail** - Full program information
6. **Dashboard** - Saved results (auth required)
7. **Admin Console** - Program management (admin only)
8. **Help/FAQ** - User guidance

### ✅ Sample Programs (6 Total)
1. CA Fresh Produce Rx (state-level, requires Medicaid + chronic condition)
2. LA County MTM (county-level, Medicaid + serious condition)
3. National SNAP Nutrition Incentive (national, income-based)
4. NYC Diabetes Prevention (county-level, diabetes focus)
5. Harris County Food Bank (county-level, Medicaid/low-income)
6. MA Healthy Incentives (state-level, requires SNAP)

## Test Endpoints

### Health Check
```bash
curl http://localhost:8001/api/health
```

### ZIP Lookup
```bash
curl -X POST http://localhost:8001/api/geography/lookup \
  -H "Content-Type: application/json" \
  -d '{"zip_code": "90001"}'
```

### Eligibility Evaluation
```bash
curl -X POST http://localhost:8001/api/eligibility/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "zip_code": "90001",
    "answers": {
      "enrolled_medicaid": "Yes",
      "enrolled_snap": "No",
      "household_size": 2,
      "income_band": "100-138% FPL",
      "age_range": "18-59",
      "pregnancy": "No",
      "health_conditions": ["Diabetes"],
      "has_case_manager": "Yes"
    }
  }'
```

### List Programs
```bash
curl http://localhost:8001/api/programs
```

## Environment Variables

### Backend (.env)
- `MONGO_URL`: MongoDB connection
- `DB_NAME`: Database name
- `EMERGENT_LLM_KEY`: Universal LLM key
- `ADMIN_EMAIL`: Admin user email (sunilbg100@gmail.com)
- `CORS_ORIGINS`: CORS configuration

### Frontend (.env)
- `REACT_APP_BACKEND_URL`: Backend API URL

## Database Collections
- `users` - User accounts
- `user_sessions` - Auth sessions
- `user_saved_results` - Saved eligibility results
- `programs` - Program catalog
- `program_rules` - Eligibility rules
- `zip_county_mapping` - Geography data

## Key Design Decisions
1. **NO LLM for eligibility** - Only deterministic rule matching
2. **Custom UUIDs** - Not MongoDB ObjectIDs (for JSON serialization)
3. **Phase 2 features NOT built** - Status tracking, email reminders
4. **NO "Emergent" branding** - Clean, neutral UI
5. **Admin restricted** - Only sunilbg100@gmail.com

## URLs
- Frontend: https://program-matcher-test.preview.emergentagent.com
- Backend: https://program-matcher-test.preview.emergentagent.com/api

## Next Steps
1. Test full user flow (questionnaire → results → save → download)
2. Test authentication flow
3. Test admin console
4. Mobile responsive testing
5. Add more ZIP codes for broader coverage
6. Add more sample programs
