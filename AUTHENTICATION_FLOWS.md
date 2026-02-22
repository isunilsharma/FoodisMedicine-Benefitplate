# BenefitPlate Authentication Flows

## 👤 Regular User Flow

### 1. Initial State (Not Logged In)
- Landing page shows: "Sign In" button in navigation
- User can browse programs (public)
- User can start eligibility questionnaire
- User CANNOT save results or download PDF

### 2. Login Process
**Step 1:** User clicks "Sign In" button
- Triggers: `AuthContext.login()` function
- Redirects to: `https://auth.emergentagent.com/?redirect={origin}/dashboard`
- Example: `https://auth.emergentagent.com/?redirect=https://healthrx-creator.preview.emergentagent.com/dashboard`

**Step 2:** Google OAuth Screen
- User sees: "LOG IN TO Benefitplate"
- User clicks: "Continue with Google"
- Google authentication: User selects account and authorizes

**Step 3:** Redirect Back with Session ID
- Redirected to: `{origin}/dashboard#session_id=XXXXX`
- Example: `https://healthrx-creator.preview.emergentagent.com/dashboard#session_id=abc123`

**Step 4:** Session Exchange (AuthCallback)
- AuthCallback component detects `session_id` in URL hash
- Calls: `POST /api/auth/session` with session_id
- Backend exchanges session_id for user data + session_token
- Backend returns: `{ user: {...}, session_token: "..." }`
- Sets httpOnly cookie: `session_token`

**Step 5:** Logged In State
- AuthContext updates: `user` state, `isAuthenticated = true`
- Navigation shows: User's name + "Logout" button (NOT "Sign In")
- User navigates to: `/dashboard` page
- User can now: Save results, download PDF

### 3. Logged In Experience
**Available Actions:**
- ✅ Browse all programs
- ✅ Complete eligibility questionnaire
- ✅ Save results (requires auth)
- ✅ Download PDF checklist (requires auth)
- ✅ View saved results in dashboard
- ✅ Logout

**Navigation Shows:**
- User's name (from Google account)
- "Logout" button
- NO "Sign In" button

---

## 👨‍💼 Admin Flow (sunilbg100@gmail.com)

### 1. Login Process
**Same as regular user** (steps 1-5 above)

### 2. Admin Detection
After successful login, backend checks:
```javascript
if (user.email === 'sunilbg100@gmail.com') {
  // User is admin
}
```

### 3. Admin UI Elements
**Navigation Shows:**
- User's name: "Sunil BG" (or whatever Google account name)
- "Admin" link (ONLY for sunilbg100@gmail.com)
- "Logout" button

**Desktop Navigation:**
```
Home | Check Eligibility | Browse Programs | Help | Sunil BG | Admin | [Logout]
```

**Mobile Navigation (Burger Menu):**
```
Home
Check Eligibility
Browse Programs
Help
Sunil BG
Admin  ← Only for admin
Logout
```

### 4. Admin Console Access
**Route:** `/admin`

**Features:**
- Tab 1: Programs (manage all programs)
  - Create new program
  - Edit existing programs
  - Delete programs
  - View all program details
  
- Tab 2: Analytics
  - Total events
  - ZIP searches
  - Questionnaires completed
  - Saved results
  - Checklist downloads
  - Unique users
  - Recent activity (last 50 events)

### 5. Admin Actions
✅ All regular user actions
✅ Create programs
✅ Edit programs
✅ Delete programs
✅ View analytics dashboard
✅ Export programs (future)
✅ Import programs (future)

---

## 🔄 Logout Flow (Both User & Admin)

### 1. User Clicks "Logout"
- Triggers: `AuthContext.logout()` function
- Calls: `POST /api/auth/logout`
- Backend deletes session from database
- Backend clears session_token cookie

### 2. Logged Out State
- AuthContext updates: `user = null`, `isAuthenticated = false`
- Navigation shows: "Sign In" button (NOT user name)
- User redirected to: Home page
- Protected routes blocked

---

## 🚨 Common Issues & Fixes

### Issue 1: "Sign In" still shows after login
**Cause:** Session exchange failed or AuthContext not updating
**Check:**
1. Browser console for errors
2. Network tab: Check /api/auth/session call
3. Cookies: Check if session_token is set

### Issue 2: Redirected back to login
**Cause:** session_id not in URL or AuthCallback not catching it
**Check:**
1. URL after redirect: Should have #session_id=XXX
2. AuthCallback component rendering
3. Browser console logs

### Issue 3: Admin console not accessible
**Cause:** Email doesn't match exactly
**Check:**
1. Logged in email (case-sensitive)
2. Backend ADMIN_EMAIL environment variable
3. Must be exactly: sunilbg100@gmail.com

---

## 🧪 Test Checklist

### Regular User Test:
- [ ] Click "Sign In" → Redirects to auth.emergentagent.com
- [ ] Login with Google → Redirects back with session_id
- [ ] Landing on /dashboard → Shows user name in nav
- [ ] "Sign In" button replaced with user name
- [ ] Can save eligibility results
- [ ] Can download PDF checklist
- [ ] Dashboard shows saved results

### Admin Test (sunilbg100@gmail.com):
- [ ] All regular user tests pass
- [ ] "Admin" link appears in navigation
- [ ] Can access /admin route
- [ ] Programs tab shows 6 programs
- [ ] Analytics tab shows stats
- [ ] Can create new program
- [ ] Can edit existing program
- [ ] Can delete program

### Logout Test:
- [ ] Click "Logout"
- [ ] Redirected to home page
- [ ] Navigation shows "Sign In" button
- [ ] User name removed from nav
- [ ] Cannot access /dashboard
- [ ] Cannot access /admin
