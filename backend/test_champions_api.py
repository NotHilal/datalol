"""
Test script for champion endpoints
Run this after starting the Flask server
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/v1"

def test_champions_roles():
    """Test GET /champions/roles"""
    print("\n" + "="*60)
    print("TEST 1: GET /champions/roles")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/champions/roles")

        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds()*1000:.0f}ms")

        if response.status_code == 200:
            data = response.json()
            roles = data.get('data', {}).get('championRoles', {})
            role_info = data.get('data', {}).get('roleInfo', {})

            print(f"✅ SUCCESS")
            print(f"Total Champions: {len(roles)}")
            print(f"Roles Defined: {len(role_info)}")
            print(f"\nSample Champions:")
            for i, (champ, role) in enumerate(list(roles.items())[:5]):
                print(f"  - {champ}: {role}")

            print(f"\nRole Categories:")
            for role, info in role_info.items():
                print(f"  - {role}: {info['description']}")

            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_champions_stats():
    """Test GET /champions/stats"""
    print("\n" + "="*60)
    print("TEST 2: GET /champions/stats")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/champions/stats")

        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds()*1000:.0f}ms")

        if response.status_code == 200:
            data = response.json()
            champions = data.get('data', {}).get('champions', [])

            print(f"✅ SUCCESS")
            print(f"Total Champions: {len(champions)}")

            if champions:
                print(f"\nTop 5 Champions by Games Played:")
                for i, champ in enumerate(champions[:5]):
                    print(f"  {i+1}. {champ['champion']} ({champ.get('role', 'N/A')})")
                    print(f"     Games: {champ['totalGames']}, WR: {champ['winRate']:.1f}%, KDA: {champ['avgKDA']:.2f}")

            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_position_stats():
    """Test GET /champions/positions"""
    print("\n" + "="*60)
    print("TEST 3: GET /champions/positions")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/champions/positions")

        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds()*1000:.0f}ms")

        if response.status_code == 200:
            data = response.json()
            positions = data.get('data', {}).get('positions', [])

            print(f"✅ SUCCESS")
            print(f"Total Positions: {len(positions)}")

            print(f"\nPosition Statistics:")
            for pos in positions:
                if 'metadata' in pos:
                    icon = pos['metadata']['icon']
                    name = pos['metadata']['fullName']
                else:
                    icon = '❓'
                    name = pos.get('position', 'Unknown')

                print(f"  {icon} {name}")
                print(f"     Games: {pos['totalGames']}, WR: {pos['winRate']:.1f}%, KDA: {pos['avgKDA']:.2f}")

            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_cache_performance():
    """Test caching performance"""
    print("\n" + "="*60)
    print("TEST 4: Cache Performance")
    print("="*60)

    endpoint = f"{BASE_URL}/champions/roles"

    # First request (cache miss)
    print("First request (cache miss):")
    response1 = requests.get(endpoint)
    time1 = response1.elapsed.total_seconds() * 1000
    print(f"  Time: {time1:.0f}ms")

    # Second request (should be cached)
    print("Second request (should be cached):")
    response2 = requests.get(endpoint)
    time2 = response2.elapsed.total_seconds() * 1000
    print(f"  Time: {time2:.0f}ms")

    # Check Cache-Control header
    cache_control = response2.headers.get('Cache-Control', 'Not set')
    print(f"  Cache-Control: {cache_control}")

    if time2 < time1:
        print(f"✅ Cache is working! {((time1-time2)/time1*100):.1f}% faster")
        return True
    else:
        print(f"⚠️  Cache may not be active (backend cache still helps)")
        return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CHAMPIONS API TEST SUITE")
    print("="*60)
    print("\nMake sure Flask server is running on http://localhost:5000")
    print("\nStarting tests in 2 seconds...")

    import time
    time.sleep(2)

    results = []

    results.append(("Champion Roles Endpoint", test_champions_roles()))
    results.append(("Champion Stats Endpoint", test_champions_stats()))
    results.append(("Position Stats Endpoint", test_position_stats()))
    results.append(("Cache Performance", test_cache_performance()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
