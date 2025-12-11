"""
Application entry point
"""
import os
from app import create_app

# Get configuration from environment variable
config_name = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(config_name)

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = config_name == 'development'

    print("=" * 60)
    print(f"Starting Flask server on http://{host}:{port}")
    print(f"Environment: {config_name}")
    print(f"Debug mode: {debug}")
    print("=" * 60)

    app.run(host=host, port=port, debug=debug)
