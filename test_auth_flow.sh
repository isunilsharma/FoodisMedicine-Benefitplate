#!/bin/bash
# Auth Flow Test Script

echo "=== BenefitPlate Auth Flow Test ==="
echo ""

# Test 1: Backend auth endpoint
echo "1. Testing backend /api/auth/me (should return 401 when not logged in):"
curl -s -w "\nHTTP Status: %{http_code}\n" http://localhost:8001/api/auth/me
echo ""

# Test 2: Check if MongoDB has users collection
echo "2. Checking MongoDB users collection:"
mongosh --quiet --eval "use('test_database'); print('Users count:', db.users.countDocuments()); print('Sessions count:', db.user_sessions.countDocuments());"
echo ""

# Test 3: Simulate session exchange (you'll need a real session_id from auth)
echo "3. To test full flow manually:"
echo "   a. Open browser to: https://program-matcher-test.preview.emergentagent.com"
echo "   b. Click 'Sign In' button"
echo "   c. Login with Google (sunilbg100@gmail.com)"
echo "   d. Check browser console for logs"
echo "   e. Check Network tab for /api/auth/session call"
echo ""

echo "4. Expected flow:"
echo "   ✓ Click Sign In → Redirects to auth.emergentagent.com"
echo "   ✓ Login with Google → Redirects to /dashboard#session_id=XXX"
echo "   ✓ AuthCallback catches session_id → Calls /api/auth/session"
echo "   ✓ Backend returns user data + sets cookie"
echo "   ✓ Frontend shows user name in nav (NOT 'Sign In')"
echo ""

echo "5. Common Issues:"
echo "   ❌ Still shows 'Sign In' after login:"
echo "      - Check browser console for errors"
echo "      - Check Network tab: /api/auth/session should return 200"
echo "      - Check Application tab → Cookies: session_token should exist"
echo ""
echo "   ❌ 'Admin' link not showing:"
echo "      - Verify email is exactly: sunilbg100@gmail.com"
echo "      - Check browser console: user.email value"
echo ""

echo "6. Debug checklist:"
echo "   - Browser console logs"
echo "   - Network tab (filter: /api/auth)"
echo "   - Application → Cookies → session_token"
echo "   - Backend logs: tail -f /var/log/supervisor/backend.out.log"
