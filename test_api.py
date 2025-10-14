"""
Test script to verify Flask API server is working correctly
"""

import requests
import time

def test_health_check():
    """Test the health check endpoint"""
    print("\n[TEST 1] Health Check Endpoint")
    print("-" * 50)
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("   Start with: python api_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_diagnose_endpoint():
    """Test the diagnose endpoint (requires server running)"""
    print("\n[TEST 2] Diagnose Endpoint")
    print("-" * 50)
    
    # Create a test payload
    data = {
        'condition': 'Testing the API endpoint - chest pain and cough',
        'email': 'test@example.com'
    }
    
    # Note: This requires an actual image file
    # For now, we'll just check if the endpoint exists
    try:
        response = requests.post(
            "http://localhost:5000/api/diagnose",
            data=data,
            stream=True,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Diagnose endpoint is accessible")
            print("   Note: Full test requires image upload")
            return True
        else:
            print(f"⚠️  Endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("=" * 50)
    print("MaiOpinion API Server Test Suite")
    print("=" * 50)
    
    # Test 1: Health Check
    health_ok = test_health_check()
    
    if not health_ok:
        print("\n❌ Server is not running or not accessible")
        print("   Start the server with: python api_server.py")
        return
    
    # Test 2: Diagnose endpoint availability
    diagnose_ok = test_diagnose_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print(f"Health Check:      {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Diagnose Endpoint: {'✅ PASS' if diagnose_ok else '❌ FAIL'}")
    print("=" * 50)
    
    if health_ok and diagnose_ok:
        print("\n✅ All tests passed! Server is ready.")
        print("\nNext steps:")
        print("1. Start frontend: cd frontend && npm run dev")
        print("2. Open browser: http://localhost:3000")
    else:
        print("\n❌ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
