"""Test rate limiting on login endpoint."""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_rate_limit():
    """Test that login endpoint is rate limited to 5 requests per minute."""

    # Test credentials (will fail but that's ok, we're testing rate limiting)
    credentials = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }

    print("Testing rate limiting on /auth/login endpoint...")
    print("Limit: 5 requests per minute per IP\n")

    success_count = 0
    rate_limited_count = 0

    # Try to make 7 login attempts
    for i in range(1, 8):
        response = requests.post(f"{BASE_URL}/auth/login", json=credentials)

        if response.status_code == 429:
            rate_limited_count += 1
            print(f"Request {i}: ❌ Rate limited (429 Too Many Requests)")
            print(f"  Response: {response.json()}")
        elif response.status_code in [401, 404]:
            success_count += 1
            print(f"Request {i}: ✓ Request allowed (got {response.status_code} - auth failed as expected)")
        else:
            print(f"Request {i}: Status {response.status_code}")

        time.sleep(0.5)  # Small delay between requests

    print(f"\n--- Results ---")
    print(f"Requests allowed: {success_count}")
    print(f"Requests rate-limited: {rate_limited_count}")

    if success_count <= 5 and rate_limited_count >= 2:
        print("\n✓ Rate limiting is working correctly!")
        return True
    else:
        print("\n❌ Rate limiting may not be working as expected")
        return False

if __name__ == "__main__":
    try:
        test_rate_limit()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to backend at http://localhost:8000")
        print("Please start the backend server first:")
        print("  cd backend && source venv/bin/activate && uvicorn src.main:app --reload")
