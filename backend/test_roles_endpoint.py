"""Test the champion roles endpoint"""
import sys
import traceback

try:
    from app import create_app
    from app.routes.champions import get_champion_roles

    app = create_app()

    with app.app_context():
        result = get_champion_roles()

        if hasattr(result, 'get_json'):
            data = result.get_json()
            print("✓ Endpoint works successfully!")
            print(f"  Total champion roles: {len(data['data']['championRoles'])}")
            print(f"  Total role types: {len(data['data']['roleInfo'])}")

            # Show a sample
            champion_roles = data['data']['championRoles']
            print("\n  Sample champion roles:")
            for i, (champ, role) in enumerate(list(champion_roles.items())[:10]):
                print(f"    {champ}: {role}")
        else:
            print("✗ Unexpected response format")
            print(result)

except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)
