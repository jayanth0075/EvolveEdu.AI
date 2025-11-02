"""
Test User Registration and Login Flow
Tests signup for new users and signin for existing users
"""

import requests
import json
import random
import string

BASE_URL = "http://localhost:8000/api"

def generate_random_user():
    """Generate random user credentials"""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        "email": f"newuser_{random_suffix}@test.com",
        "username": f"newuser_{random_suffix}",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "role": "student"
    }

def test_new_user_signup():
    """Test signup for a brand new user"""
    print("\n" + "="*60)
    print("🆕 TEST 1: NEW USER SIGNUP")
    print("="*60)
    
    user_data = generate_random_user()
    print(f"\n📝 Creating new user:")
    print(f"   Email: {user_data['email']}")
    print(f"   Username: {user_data['username']}")
    print(f"   Role: {user_data['role']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=user_data,
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("\n✅ SIGNUP SUCCESSFUL!")
            print(f"\n📊 User Details:")
            print(f"   ID: {result['user'].get('id')}")
            print(f"   Email: {result['user'].get('email')}")
            print(f"   Username: {result['user'].get('username')}")
            print(f"   Role: {result['user'].get('role')}")
            print(f"\n🔑 Tokens Received:")
            print(f"   Access Token: {result['access'][:30]}...")
            print(f"   Refresh Token: {result['refresh'][:30]}...")
            return user_data, result['access']
        else:
            print("\n❌ SIGNUP FAILED!")
            print(f"   Error: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None, None

def test_existing_user_login(user_data):
    """Test login for an existing user"""
    print("\n" + "="*60)
    print("🔑 TEST 2: EXISTING USER LOGIN")
    print("="*60)
    
    login_data = {
        "email": user_data['email'],
        "password": user_data['password']
    }
    
    print(f"\n📝 Logging in with:")
    print(f"   Email: {login_data['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json=login_data,
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ LOGIN SUCCESSFUL!")
            print(f"\n📊 User Details:")
            print(f"   ID: {result['user'].get('id')}")
            print(f"   Email: {result['user'].get('email')}")
            print(f"   Username: {result['user'].get('username')}")
            print(f"\n🔑 New Tokens Received:")
            print(f"   Access Token: {result['access'][:30]}...")
            print(f"   Refresh Token: {result['refresh'][:30]}...")
            return result['access']
        else:
            print("\n❌ LOGIN FAILED!")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def test_wrong_password(user_data):
    """Test login with wrong password"""
    print("\n" + "="*60)
    print("🚫 TEST 3: LOGIN WITH WRONG PASSWORD")
    print("="*60)
    
    login_data = {
        "email": user_data['email'],
        "password": "WrongPassword123!"
    }
    
    print(f"\n📝 Attempting login with wrong password:")
    print(f"   Email: {login_data['email']}")
    print(f"   Password: (intentionally wrong)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json=login_data,
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 400:
            print("\n✅ CORRECTLY REJECTED!")
            print("   System properly validates passwords")
            print(f"   Error: {response.json()}")
            return True
        else:
            print("\n❌ SECURITY ISSUE!")
            print("   Wrong password should be rejected")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_duplicate_signup(user_data):
    """Test signup with already registered email"""
    print("\n" + "="*60)
    print("🔄 TEST 4: DUPLICATE EMAIL SIGNUP")
    print("="*60)
    
    print(f"\n📝 Attempting to register same email again:")
    print(f"   Email: {user_data['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=user_data,
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 400:
            print("\n✅ CORRECTLY REJECTED!")
            print("   System prevents duplicate registrations")
            print(f"   Error: {response.json()}")
            return True
        else:
            print("\n❌ DATA INTEGRITY ISSUE!")
            print("   Duplicate emails should be rejected")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_profile_access(token):
    """Test accessing user profile with token"""
    print("\n" + "="*60)
    print("👤 TEST 5: PROFILE ACCESS WITH TOKEN")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n📝 Accessing profile with token:")
    print(f"   Token: {token[:30]}...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/profile/",
            headers=headers,
            timeout=10
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            profile = response.json()
            print("\n✅ PROFILE ACCESS SUCCESSFUL!")
            print(f"\n📊 Profile Data:")
            print(f"   ID: {profile.get('id')}")
            print(f"   Email: {profile.get('email')}")
            print(f"   Username: {profile.get('username')}")
            print(f"   Role: {profile.get('role')}")
            print(f"   Created: {profile.get('created_at', 'N/A')[:10]}")
            if profile.get('progress'):
                print(f"\n📈 Progress Data:")
                print(f"   Study Time: {profile['progress'].get('total_study_time', 0)} minutes")
                print(f"   Streak: {profile['progress'].get('streak_days', 0)} days")
            return True
        else:
            print("\n❌ PROFILE ACCESS FAILED!")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_password_validation():
    """Test password validation rules"""
    print("\n" + "="*60)
    print("🔒 TEST 6: PASSWORD VALIDATION")
    print("="*60)
    
    weak_passwords = [
        ("12345678", "Too common/numeric only"),
        ("password", "Too common word"),
        ("abc", "Too short")
    ]
    
    results = []
    
    for weak_pass, reason in weak_passwords:
        user_data = generate_random_user()
        user_data['password'] = weak_pass
        user_data['password_confirm'] = weak_pass
        
        print(f"\n📝 Testing weak password: '{weak_pass}' ({reason})")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/register/",
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 400:
                print(f"   ✅ Correctly rejected")
                results.append(True)
            else:
                print(f"   ❌ Weak password accepted (SECURITY ISSUE)")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append(False)
    
    if all(results):
        print("\n✅ PASSWORD VALIDATION WORKING!")
        return True
    else:
        print("\n⚠️  Some weak passwords were accepted")
        return False

def main():
    print("="*60)
    print("🧪 USER AUTHENTICATION TEST SUITE")
    print("="*60)
    print("\nTesting signup and signin functionality...")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print("\n✅ Server is running")
    except:
        print("\n❌ ERROR: Server is not running!")
        print("   Please start the server with: python manage.py runserver")
        return
    
    results = {}
    
    # Test 1: New user signup
    user_data, token = test_new_user_signup()
    results['Signup'] = user_data is not None
    
    if user_data:
        # Test 2: Login with created user
        login_token = test_existing_user_login(user_data)
        results['Login'] = login_token is not None
        
        # Test 3: Wrong password
        results['Wrong Password Rejection'] = test_wrong_password(user_data)
        
        # Test 4: Duplicate email
        results['Duplicate Email Rejection'] = test_duplicate_signup(user_data)
        
        # Test 5: Profile access
        if token:
            results['Profile Access'] = test_profile_access(token)
    
    # Test 6: Password validation
    results['Password Validation'] = test_password_validation()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print("="*60)
    print(f"\n🎯 Final Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL AUTHENTICATION TESTS PASSED! 🎉")
        print("\n📋 Summary:")
        print("   ✅ New user signup works")
        print("   ✅ Existing user login works")
        print("   ✅ Password validation works")
        print("   ✅ Duplicate prevention works")
        print("   ✅ Token-based access works")
        print("\n🚀 Your authentication system is production-ready!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\n📋 Review the failures above")

if __name__ == "__main__":
    main()
