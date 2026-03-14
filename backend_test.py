#!/usr/bin/env python3
"""
BenefitPlate Backend API Testing
Tests all backend endpoints for functionality and integration
"""
import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any

class BenefitPlateAPITester:
    def __init__(self, base_url="https://program-matcher-test.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name: str, method: str, endpoint: str, expected_status: int, 
                 data: Dict[Any, Any] = None, headers: Dict[str, str] = None) -> tuple[bool, Dict[Any, Any]]:
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        if headers:
            test_headers.update(headers)
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, {"message": "Success but no JSON response"}
            else:
                error_detail = f"Expected {expected_status}, got {response.status_code}"
                try:
                    error_content = response.json()
                    error_detail += f" - Response: {error_content}"
                except:
                    error_detail += f" - Response: {response.text[:200]}"
                
                print(f"❌ Failed - {error_detail}")
                self.failed_tests.append({
                    "test": name,
                    "endpoint": endpoint,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "error": error_detail
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "endpoint": endpoint,
                "error": str(e)
            })
            return False, {}

    def test_health_endpoints(self):
        """Test basic health and info endpoints"""
        print("\n🏥 Testing Health Endpoints")
        
        # Test root endpoint
        self.run_test("API Root", "GET", "api/", 200)
        
        # Test health check
        self.run_test("Health Check", "GET", "api/health", 200)

    def test_geography_endpoints(self):
        """Test geography/ZIP lookup functionality"""
        print("\n🗺️ Testing Geography Endpoints")
        
        # Test ZIP lookup with known ZIP (90001 - Los Angeles County, CA)
        zip_data = {"zip_code": "90001"}
        success, response = self.run_test(
            "ZIP Lookup - 90001", 
            "POST", 
            "api/geography/lookup", 
            200, 
            zip_data
        )
        
        if success:
            print(f"   ZIP Result: {response}")
            # Verify expected location
            if response.get("county") == "Los Angeles County" and response.get("state") == "California":
                print("   ✅ ZIP location correct")
            else:
                print("   ⚠️ ZIP location may be incorrect")
        
        # Test invalid ZIP
        invalid_zip_data = {"zip_code": "00000"}
        self.run_test(
            "ZIP Lookup - Invalid", 
            "POST", 
            "api/geography/lookup", 
            404, 
            invalid_zip_data
        )

    def test_programs_endpoints(self):
        """Test programs listing and detail endpoints"""
        print("\n📋 Testing Programs Endpoints")
        
        # Test list all programs
        success, response = self.run_test("List All Programs", "GET", "api/programs", 200)
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} programs")
            if len(response) >= 6:
                print("   ✅ Expected 6+ seeded programs found")
            else:
                print("   ⚠️ Less than 6 programs found")
            
            # Test program detail with first program
            if response:
                first_program = response[0]
                program_id = first_program.get("program_id")
                if program_id:
                    self.run_test(
                        f"Program Detail - {program_id[:8]}...", 
                        "GET", 
                        f"api/programs/{program_id}", 
                        200
                    )
        
        # Test programs with filters
        self.run_test("List Programs - California", "GET", "api/programs?state=California", 200)
        self.run_test("List Programs - Food Benefits", "GET", "api/programs?benefit_type=Food", 200)

    def test_eligibility_endpoints(self):
        """Test eligibility evaluation"""
        print("\n🎯 Testing Eligibility Endpoints")
        
        # Sample questionnaire answers (based on QuestionnaireAnswers model)
        eligibility_data = {
            "zip_code": "90001",
            "answers": {
                "enrolled_medicaid": "Yes",
                "enrolled_snap": "No",
                "household_size": 2,
                "income_band": "Under 100% FPL",
                "age_range": "18-59",
                "pregnancy": "No",
                "health_conditions": ["diabetes"],
                "has_case_manager": "No"
            }
        }
        
        success, response = self.run_test(
            "Eligibility Evaluation", 
            "POST", 
            "api/eligibility/evaluate", 
            200, 
            eligibility_data
        )
        
        if success:
            print(f"   Results categories:")
            print(f"   - Likely eligible: {len(response.get('likely_eligible', []))}")
            print(f"   - Possibly eligible: {len(response.get('possibly_eligible', []))}")
            print(f"   - Community programs: {len(response.get('community', []))}")

    def test_admin_endpoints(self):
        """Test admin endpoints (will fail without auth, which is expected)"""
        print("\n👑 Testing Admin Endpoints (Expected to fail without auth)")
        
        # These should fail with 401/403 (which is correct behavior)
        self.run_test("Admin Analytics", "GET", "api/admin/analytics", 401)
        self.run_test("Admin Programs List", "GET", "api/admin/programs", 401)

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting BenefitPlate Backend API Tests")
        print(f"Base URL: {self.base_url}")
        print("=" * 60)
        
        try:
            self.test_health_endpoints()
            self.test_geography_endpoints()
            self.test_programs_endpoints()
            self.test_eligibility_endpoints()
            self.test_admin_endpoints()
        except Exception as e:
            print(f"\n💥 Critical error during testing: {e}")
            return False
        
        # Print results
        print(f"\n📊 Test Results:")
        print(f"Tests passed: {self.tests_passed}/{self.tests_run}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ Failed Tests:")
            for failure in self.failed_tests:
                print(f"  - {failure['test']}: {failure.get('error', 'Status code mismatch')}")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test runner"""
    tester = BenefitPlateAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())