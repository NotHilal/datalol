"""
Quick test to verify champion roles API response
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/v1"

def test_roles_endpoint():
    print("\n" + "="*60)
    print("Testing /champions/roles endpoint")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/champions/roles")
        print(f"\nStatus Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # Check structure
            print(f"\nResponse keys: {list(data.keys())}")
            print(f"Data keys: {list(data.get('data', {}).keys())}")

            champion_roles = data.get('data', {}).get('championRoles', {})
            print(f"\nTotal champions with roles: {len(champion_roles)}")

            # Show first 10 champions
            print("\nFirst 10 champions:")
            for i, (champ, role) in enumerate(list(champion_roles.items())[:10]):
                print(f"  {i+1}. {champ}: {role}")

            # Check role distribution
            from collections import Counter
            role_counts = Counter(champion_roles.values())
            print(f"\nRole distribution:")
            for role, count in sorted(role_counts.items(), key=lambda x: -x[1]):
                print(f"  {role}: {count}")

            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("\nMake sure Flask server is running on http://localhost:5000")
    import time
    time.sleep(1)

    test_roles_endpoint()
