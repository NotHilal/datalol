"""
Test to compare champion names from roles vs stats endpoints
"""
import requests

BASE_URL = "http://localhost:5000/api/v1"

def compare_champion_names():
    print("\n" + "="*60)
    print("Comparing Champion Names: Roles vs Stats")
    print("="*60)

    try:
        # Get roles
        roles_response = requests.get(f"{BASE_URL}/champions/roles")
        roles_data = roles_response.json().get('data', {}).get('championRoles', {})

        # Get stats
        stats_response = requests.get(f"{BASE_URL}/champions/stats")
        stats_data = stats_response.json().get('data', {}).get('champions', [])

        role_names = set(roles_data.keys())
        stat_names = set(stat['champion'] for stat in stats_data)

        print(f"\nChampions in roles dictionary: {len(role_names)}")
        print(f"Champions in stats: {len(stat_names)}")

        # Find champions in stats but not in roles
        missing_in_roles = stat_names - role_names
        if missing_in_roles:
            print(f"\n⚠️  Champions in STATS but NOT in ROLES ({len(missing_in_roles)}):")
            for name in sorted(list(missing_in_roles)[:20]):
                print(f"  - {name}")
                # Try to find case-insensitive match
                lower_match = [r for r in role_names if r.lower() == name.lower()]
                if lower_match:
                    print(f"    ^ Found case mismatch: '{lower_match[0]}' exists in roles")
        else:
            print("\n✅ All stats champions found in roles dictionary")

        # Find champions in roles but not in stats
        missing_in_stats = role_names - stat_names
        if missing_in_stats:
            print(f"\nChampions in ROLES but NOT in STATS ({len(missing_in_stats)}):")
            for name in sorted(list(missing_in_stats)[:10]):
                print(f"  - {name}")

        # Sample comparison
        print(f"\nSample champion names from STATS:")
        for stat in stats_data[:5]:
            champ_name = stat['champion']
            has_role = champ_name in roles_data
            print(f"  '{champ_name}' -> Role found: {has_role}")
            if not has_role:
                # Try case-insensitive
                matches = [r for r in role_names if r.lower() == champ_name.lower()]
                if matches:
                    print(f"    ^ Case-insensitive match: '{matches[0]}'")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\nMake sure Flask server is running on http://localhost:5000\n")
    import time
    time.sleep(1)

    compare_champion_names()
